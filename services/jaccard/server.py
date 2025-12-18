import grpc
import time
import copy
import threading
from concurrent import futures
import methods_pb2
import methods_pb2_grpc
from itertools import combinations
import sys

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class ProteinAnalyzer:
    def __init__(self):
        self.proteins = {}
        self.entry_to_id = {}
        self.domain_sets = {}
        self.pair_cache = {}
        self.history = []
        self.named_states = {}
        self.lock = threading.Lock()
        self.is_dirty = False 

    def _get_current_state_snapshot(self):
        return {
            'proteins': copy.deepcopy(self.proteins),
            'entry_to_id': copy.deepcopy(self.entry_to_id),
            'domain_sets': copy.deepcopy(self.domain_sets),
            'pair_cache': copy.deepcopy(self.pair_cache)
        }

    def _restore_state_from_snapshot(self, snapshot):
        with self.lock:
            self.proteins = snapshot['proteins']
            self.entry_to_id = snapshot['entry_to_id']
            self.domain_sets = snapshot['domain_sets']
            if 'pair_cache' in snapshot:
                self.pair_cache = snapshot['pair_cache']
            self.is_dirty = False 

    def create_history_snapshot(self):
        self.history.append(self._get_current_state_snapshot())

    def save_named_state(self, name, overwrite):
        with self.lock:
            if name in self.named_states and not overwrite:
                return False, f"State '{name}' already exists. Use overwrite=True."
            self.named_states[name] = self._get_current_state_snapshot()
            return True, f"State saved as '{name}'. Proteins: {len(self.proteins)}"

    def load_named_state(self, name):
        snapshot = self.named_states.get(name)
        if not snapshot:
            return False, f"State '{name}' not found."
        self._restore_state_from_snapshot(snapshot)
        return True, f"Rolled back to '{name}'. Total proteins: {len(self.proteins)}"

    def remove_named_state(self, name):
        with self.lock:
            if name in self.named_states:
                del self.named_states[name]
                return True, f"State '{name}' removed."
            return False, f"State '{name}' not found."

    def get_state_names(self):
        return list(self.named_states.keys())

    def perform_standard_rollback(self):
        if not self.history:
            return False, "No history."
        snapshot = self.history.pop()
        self._restore_state_from_snapshot(snapshot)
        return True, f"Rollback successful. Total proteins: {len(self.proteins)}"

    def add_batch(self, batch_proto):
        with self.lock:
            for p in batch_proto.proteins:
                if p.id not in self.proteins:
                    self.proteins[p.id] = p
                    self.entry_to_id[p.entry] = p.id
                    d_set = set(x for x in p.interpro.split(';') if x.strip())
                    self.domain_sets[p.id] = d_set
            self.is_dirty = True

    def _calculate_pair(self, p1_id, p2_id):
        """Calculate Jaccard for a pair. Always uses canonical key (sorted tuple)."""
        # Skip self-comparison
        if p1_id == p2_id:
            return None
            
        key = tuple(sorted((p1_id, p2_id)))
        if key in self.pair_cache:
            return self.pair_cache[key]
        
        s1 = self.domain_sets.get(p1_id, set())
        s2 = self.domain_sets.get(p2_id, set())
        union_len = len(s1.union(s2))
        score = len(s1.intersection(s2)) / union_len if union_len > 0 else 0.0
        
        # Store with canonical key for bidirectional lookup
        self.pair_cache[key] = score
        return score

    def compute_pairs_for_protein(self, p1_id, all_ids):
        """Compute all pairs involving p1_id with IDs that come after it (to avoid duplicates)."""
        for p2_id in all_ids:
            if p1_id != p2_id:  # Skip self-comparison
                self._calculate_pair(p1_id, p2_id)

    def compute_all(self):
        if not self.is_dirty:
            return 

        all_ids = list(self.proteins.keys())
        if len(all_ids) == 0: 
            return

        # Calculate number of unique pairs (excluding self-comparisons)
        num_pairs = (len(all_ids) * (len(all_ids) - 1)) // 2
        print(f"Server: Data dirty. Ensuring all {num_pairs} unique pairs are cached...")
        
        with futures.ThreadPoolExecutor(max_workers=8) as executor:
            futures.wait([
                executor.submit(self.compute_pairs_for_protein, p_id, all_ids) 
                for p_id in all_ids
            ])
        
        self.is_dirty = False 
        print(f"Server: Cache complete. {len(self.pair_cache)} pairs cached.")

    def delete_proteins(self, entries_to_delete):
        with self.lock:
            self.create_history_snapshot()
            ids_to_delete = {self.entry_to_id.get(entry) for entry in entries_to_delete if entry in self.entry_to_id}
            deleted_count = 0
            
            for p_id in list(ids_to_delete):
                if p_id in self.proteins:
                    del self.proteins[p_id]
                    del self.domain_sets[p_id]
                    deleted_count += 1
            
            for entry in entries_to_delete:
                if entry in self.entry_to_id:
                    del self.entry_to_id[entry]
            
            # Clean up cache entries involving deleted proteins
            keys_to_remove = [
                key for key in self.pair_cache.keys() 
                if key[0] in ids_to_delete or key[1] in ids_to_delete
            ]
            for key in keys_to_remove:
                del self.pair_cache[key]
            
            self.is_dirty = True 
            return True, f"Deleted {deleted_count} proteins."

    def recalculate_matrix(self):
        self.pair_cache.clear()
        self.is_dirty = True
        self.compute_all()
        return True, "Full matrix recalculation complete."

class PassServicer(methods_pb2_grpc.PassServicer):
    def __init__(self):
        self.analyzer = ProteinAnalyzer()

    def AddProteinBatch(self, request, context):
        self.analyzer.create_history_snapshot()
        self.analyzer.add_batch(request)
        return methods_pb2.Ack(success=True, message=f"Added {len(request.proteins)} proteins.")

    def CalculateBestMatches(self, request, context):
        """Returns all pairwise correlations for each protein (excluding self)."""
        self.analyzer.compute_all()
        
        all_ids = list(self.analyzer.proteins.keys())
        
        for p_id in all_ids:
            query_prot = self.analyzer.proteins[p_id]
            correlations = []
            
            for other_id in all_ids:
                if p_id == other_id:  # Skip self-comparison
                    continue
                    
                other_prot = self.analyzer.proteins[other_id]
                score = self.analyzer._calculate_pair(p_id, other_id)
                
                if score is not None:  # Should always be true now
                    correlations.append(
                        methods_pb2.JaccardTuple(entry=other_prot.entry, jaccard=score)
                    )
            
            yield methods_pb2.MatchResult(
                query_protein=query_prot,
                correlations=correlations
            )

    def CalculateAllPairs(self, request, context):
        """Alternative method: returns each unique pair once."""
        self.analyzer.compute_all()
        
        all_ids = sorted(self.analyzer.proteins.keys())
        
        # Iterate through unique pairs
        for i, p1_id in enumerate(all_ids):
            p1 = self.analyzer.proteins[p1_id]
            correlations = []
            
            for p2_id in all_ids[i+1:]:  # Only pairs after current to avoid duplicates
                p2 = self.analyzer.proteins[p2_id]
                score = self.analyzer._calculate_pair(p1_id, p2_id)
                
                if score is not None:
                    correlations.append(
                        methods_pb2.JaccardTuple(entry=p2.entry, jaccard=score)
                    )
            
            if correlations:  # Only yield if there are correlations
                yield methods_pb2.MatchResult(
                    query_protein=p1,
                    correlations=correlations
                )

    def SaveState(self, request, context):
        success, message = self.analyzer.save_named_state(request.state_name, request.overwrite)
        return methods_pb2.Ack(success=success, message=message)
    
    def RollbackToState(self, request, context):
        if not request.confirm:
            return methods_pb2.Ack(success=False, message="Rollback cancelled.")
        if request.state_name:
            success, message = self.analyzer.load_named_state(request.state_name)
        else:
            success, message = self.analyzer.perform_standard_rollback()
        return methods_pb2.Ack(success=success, message=message)

    def DeleteProteins(self, request, context):
        success, message = self.analyzer.delete_proteins(request.entries)
        return methods_pb2.Ack(success=success, message=message)
        
    def RecalculateBestMatches(self, request, context):
        success, message = self.analyzer.recalculate_matrix()
        return methods_pb2.Ack(success=success, message=message)

    def GetSavedStates(self, request, context):
        names = self.analyzer.get_state_names()
        return methods_pb2.StateList(names=names)

    def RemoveSavedState(self, request, context):
        success, message = self.analyzer.remove_named_state(request.name)
        return methods_pb2.Ack(success=success, message=message)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    methods_pb2_grpc.add_PassServicer_to_server(PassServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC Server started on port 50051...")
    try:
        while True: 
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()