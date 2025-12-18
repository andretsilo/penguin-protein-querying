protoc --proto_path=. --python_out=. methods.proto

python -m grpc_tools.protoc -I. --python_out=. --pyi_out=. --grpc_python_out=. methods.proto


if you want to test it:
    - start the server.py
    - start listener.py
    - do either file-import.py or list-inject.py or both / OR do a request like below
    - you can do send.py to send it as POST to the neo4j service i guess



POST Request like MOCK_HTTP_PAYLOAD:
payload = [
    { "Entry": "HTTP_PROT_01", "InterPro": "IPR001;IPR002;IPR003;", "Sequence": "MKV..." },
    { "Entry": "HTTP_PROT_02", "InterPro": "IPR001;IPR002;", "Sequence": "MKV..." },
    { "Entry": "HTTP_PROT_03", "InterPro": "IPR005;IPR006;", "Sequence": "MKV..." }
]


Request for Linux:

curl -X POST http://localhost:50052/inject \
  -H "Content-Type: application/json" \
  -d '[
    {"Entry": "HTTP_PROT_01", "InterPro": "IPR001;IPR002;IPR003;", "Sequence": "MKV..."},
    {"Entry": "HTTP_PROT_02", "InterPro": "IPR001;IPR002;", "Sequence": "MKV..."},
    {"Entry": "HTTP_PROT_03", "InterPro": "IPR005;IPR006;", "Sequence": "MKV..."}
  ]'

Request for Windows (PowerShell):

$body = @(
    @{
        Entry = "HTTP_PROT_01"
        InterPro = "IPR001;IPR002;IPR003;"
        Sequence = "MKV..."
    },
    @{
        Entry = "HTTP_PROT_02"
        InterPro = "IPR001;IPR002;"
        Sequence = "MKV..."
    }
) | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:50052/inject -Method POST -Body $body -ContentType "application/json"