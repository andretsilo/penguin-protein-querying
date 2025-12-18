import grpc
import methods_pb2
import methods_pb2_grpc
import sys

def run():
    print("--- Delete Proteins ---")
    if len(sys.argv) < 2:
        print("Usage: python delete.py <entry1,entry2,...>")
        sys.exit(1)

    entries = [e.strip() for e in sys.argv[1].split(',')]
    
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = methods_pb2_grpc.PassStub(channel)
        print(f"Deleting: {entries}")
        ack = stub.DeleteProteins(methods_pb2.EntryList(entries=entries))
        print(f"Result: {ack.message}")

if __name__ == '__main__':
    run()