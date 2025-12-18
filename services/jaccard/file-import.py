import grpc
import methods_pb2
import methods_pb2_grpc
import json

FILENAME = "test1.json"

def json_entry_to_proto(data):
    return methods_pb2.Protein(
        id=data.get('_id', {}).get('$oid', data.get('Entry')),
        entry=data.get('Entry', ''),
        reviewed=data.get('Reviewed', ''),
        entry_name=data.get('Entry Name', ''),
        protein_names=data.get('Protein names', ''),
        interpro=data.get('InterPro', ''),
        ec_number=data.get('EC number', ''),
        sequence=data.get('Sequence', '')
    )

def run():
    print(f"--- File Import ({FILENAME}) ---")
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = methods_pb2_grpc.PassStub(channel)

        try:
            with open(FILENAME, 'r') as f:
                data = json.load(f)
            
            proto_list = [json_entry_to_proto(d) for d in data]
            batch = methods_pb2.ProteinBatch(proteins=proto_list)

            print(f"Uploading {len(proto_list)} proteins...")
            ack = stub.AddProteinBatch(batch)
            print(f"Response: {ack.message}")

            print("Verifying Output...")
            for match in stub.CalculateBestMatches(methods_pb2.Empty()):
                print(f"  {match.query_protein.entry}: {len(match.correlations)} correlations found.")

        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    run()