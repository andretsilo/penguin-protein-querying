import grpc
import methods_pb2
import methods_pb2_grpc
import sys
import json

OUTPUT_JSON_FILE = "jaccard_results.json"

def proto_to_json_dict(match):
    """Convert match result to JSON format with JaccardCorrelations as list."""
    correlations_list = []
    for c in match.correlations:
        correlations_list.append({
            "Entry": c.entry,
            "Jaccard": c.jaccard
        })

    return {
        "Entry": match.query_protein.entry,
        "JaccardCorrelations": correlations_list
    }

def run():
    file_name = sys.argv[1] + "_" if len(sys.argv) > 1 else ""
    print("--- Download and Save JSON ---")
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = methods_pb2_grpc.PassStub(channel)

        print("Requesting list...")
        all_matches_json = []
        try:
            for match in stub.CalculateBestMatches(methods_pb2.Empty()):
                all_matches_json.append(proto_to_json_dict(match))
                
            if all_matches_json:
                with open(file_name + OUTPUT_JSON_FILE, 'w') as f:
                    json.dump(all_matches_json, f, indent=2)
                print(f"Saved {len(all_matches_json)} results to {file_name + OUTPUT_JSON_FILE}")
            else:
                print("No results.")
                
        except grpc.RpcError as e:
            print(f"RPC Error: {e.details()}")

if __name__ == '__main__':
    run()