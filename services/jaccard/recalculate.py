import grpc
import methods_pb2
import methods_pb2_grpc

def run():
    print("--- Recalculate All Matches ---")
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = methods_pb2_grpc.PassStub(channel)
        print("Triggering recalculation...")
        ack = stub.RecalculateBestMatches(methods_pb2.Empty())
        print(f"Result: {ack.message}")

if __name__ == '__main__':
    run()