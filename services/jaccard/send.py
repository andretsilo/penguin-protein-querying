import grpc
import methods_pb2
import methods_pb2_grpc
import json
import requests
import sys

API_URL = "http://localhost:8080/api/proteins"

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
    print("--- Client: Fetching data and POSTing via HTTP ---")
    
    all_matches_json = []
    try:
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = methods_pb2_grpc.PassStub(channel)
            print("1. Requesting data...")
            for match in stub.CalculateBestMatches(methods_pb2.Empty()):
                all_matches_json.append(proto_to_json_dict(match))
                
    except grpc.RpcError as e:
        print(f"ERROR: {e.details()}")
        sys.exit(1)

    if not all_matches_json:
        print("INFO: No data to send.")
        return

    print(f"Fetched {len(all_matches_json)} proteins.")
    print(f"2. Sending to {API_URL}")
    
    try:
        response = requests.post(
            API_URL, 
            json=all_matches_json, 
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        return response
    except Exception as e:
        print(f"Server is not open")

if __name__ == '__main__':
    run()