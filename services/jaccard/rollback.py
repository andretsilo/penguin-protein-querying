import grpc
import methods_pb2
import methods_pb2_grpc
import sys
import os

def run():
    state_name = sys.argv[1] if len(sys.argv) > 1 else ""

    print(f"--- Rollback to {state_name} State ---")
    
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = methods_pb2_grpc.PassStub(channel)

        prompt_msg = f"Rollback to state '{state_name}'? " if state_name else "Perform standard (one-step) rollback? (This state has not been saved.) "
        
        response = input(prompt_msg + "(Y/N): ").strip().upper()
        
        confirmation = (response == 'Y')

        if not confirmation:
            print("Operation cancelled by user.")
            return

        # Call RPC
        request = methods_pb2.RollbackRequest(state_name=state_name, confirm=confirmation)
        ack = stub.RollbackToState(request)
        
        if ack.success:
            print(f"SUCCESS: {ack.message}")
            print("Fetching protein count in new state...")
            count = sum(1 for _ in stub.CalculateBestMatches(methods_pb2.Empty()))
            print(f"Current protein count: {count}")
        else:
            print(f"ERROR: Rollback failed: {ack.message}")

if __name__ == '__main__':
    run()