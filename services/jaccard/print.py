import grpc
import methods_pb2
import methods_pb2_grpc

def run():
    print("--- View Current State ---")
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = methods_pb2_grpc.PassStub(channel)

        print("Requesting list...")
        count = 0
        total_correlations = 0
        try:
            for match in stub.CalculateBestMatches(methods_pb2.Empty()):
                count += 1
                num_corr = len(match.correlations)
                total_correlations += num_corr
                
                print(f"[{count}] {match.query_protein.entry}")
                print(f"    Correlations: {num_corr} pairs (excluding self)")
                
                # Print first 3 as sample
                for i, c in enumerate(match.correlations[:3]):
                    print(f"      - {c.entry}: {c.jaccard:.4f}")
                if num_corr > 3:
                    print(f"      ... and {num_corr - 3} more")
            
            if count == 0:
                print("No data.")
            else:
                avg_correlations = total_correlations / count if count > 0 else 0
                print(f"\nSummary: {count} proteins, avg {avg_correlations:.1f} correlations per protein")
                
        except grpc.RpcError as e:
            print(f"RPC Error: {e}")

if __name__ == '__main__':
    run()