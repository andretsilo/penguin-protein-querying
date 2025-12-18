import grpc
import methods_pb2
import methods_pb2_grpc
import sys
import json

SERVER_URL = "http://localhost:50051"

MOCK_HTTP_PAYLOAD = [
    { "Entry": "HTTP_PROT_01", "InterPro": "IPR001;IPR002;IPR003;", "Sequence": "MKV..." },
    { "Entry": "HTTP_PROT_02", "InterPro": "IPR001;IPR002;", "Sequence": "MKV..." },
    { "Entry": "HTTP_PROT_03", "InterPro": "IPR005;IPR006;", "Sequence": "MKV..." }
]

def dict_to_proto(d):
    return methods_pb2.Protein(
        id=d.get("Entry"),
        entry=d.get("Entry"),
        interpro=d.get("InterPro"),
        sequence=d.get("Sequence")
    )

def run():
    print("--- List Injection ---")
    with grpc.insecure_channel('localhost:50051') as channel:
        
        # Handle payload from command line argument or use mock data
        if len(sys.argv) == 2:
            try:
                # Parse JSON string from command line
                payload = json.loads(sys.argv[1])
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON argument: {e}")
                sys.exit(1)
        else:
            payload = MOCK_HTTP_PAYLOAD
        
        stub = methods_pb2_grpc.PassStub(channel)
        
        try:
            proto_list = [dict_to_proto(d) for d in payload]
            batch = methods_pb2.ProteinBatch(proteins=proto_list)

            print(f"Sending {len(proto_list)} proteins...")
            ack = stub.AddProteinBatch(batch)
            print(f"Response: {ack.message}")

            print("Verifying...")
            for match in stub.CalculateBestMatches(methods_pb2.Empty()):
                print(f"  {match.query_protein.entry}: {len(match.correlations)} correlations found.")
                
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

if __name__ == '__main__':
    run()