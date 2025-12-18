import grpc
import methods_pb2
import methods_pb2_grpc
import sys

def run():
    print("--- Save State ---")
    
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = methods_pb2_grpc.PassStub(channel)
        
        # If no argument provided, list existing states
        if len(sys.argv) < 2:
            state_list = stub.GetSavedStates(methods_pb2.Empty())
            if state_list.names:
                print("Existing saved states:")
                for i, name in enumerate(state_list.names, 1):
                    print(f"  {i}. {name}")
            else:
                print("No saved states found.")
            print("\nUsage: python save-state.py <state_name>")
            sys.exit(0)

        state_name = sys.argv[1]
        
        request = methods_pb2.SaveStateRequest(state_name=state_name, overwrite=False)
        ack = stub.SaveState(request)
        
        if ack.success:
            print(f"SUCCESS: {ack.message}")
            return

        if "already exists" in ack.message:
            response = input(f"State '{state_name}' exists. Overwrite? (Y/N): ").strip().upper()
            if response == 'Y':
                request.overwrite = True
                ack = stub.SaveState(request)
                print(f"OVERWRITE SUCCESS: {ack.message}")
            else:
                print("Cancelled.")
        else:
            print(f"ERROR: {ack.message}")

if __name__ == '__main__':
    run()