# **Protein Data Injection API via gRPC**

## Overview

This project provides a **FastAPI-based HTTP interface** that communicates with a **gRPC backend** to:

* Accept protein data annotated with InterPro domains
* Compute **pairwise Jaccard similarity scores**
* Automatically forward processed data to **Neo4j**

The system consists of:

* **FastAPI listener** → runs on **`http://localhost:50052`** / GUI on **`http://localhost:50052/docs`**
* **gRPC server (`server.py`)** → runs on **`localhost:50051`**

> When you start `listener.py`, the gRPC server is launched automatically.

---

## Quick Start

### (Optional since already done) Generate gRPC Python files

If you need to redo methods, modify the base gRPC files (methods.proto) and run one of the following (from the project root):

```bash
protoc --proto_path=. --python_out=. methods.proto
```

or

```bash
python -m grpc_tools.protoc -I. --python_out=. --pyi_out=. --grpc_python_out=. methods.proto
```

---

### Start the system

```bash
python listener.py
```

Once running, open your browser and visit:

**Swagger UI (interactive docs):**

```
http://localhost:50052/docs
```

---

## Testing the API

### Use Swagger UI (recommended)

Go to:

```
http://localhost:50052/docs
```

Then:

* Open **POST /inject**
* Click **Try it out**
* Paste your JSON payload
* Click **Execute**

---

### Using helper scripts

You can also run:

```bash
python file-import.py
python list-inject.py
```

Or send results to Neo4j manually:

```bash
python send.py
```

---

## POST /inject — Example Payload

### Mock JSON payload

```json
[
  {
    "Entry": "A0A087QH05",
    "InterPro": "IPR001;IPR002;IPR003;IPR004;IPR005;IPR006;IPR007;IPR008;IPR009;IPR010;",
    "Sequence": "MKVLWAAA"
  },
  {
    "Entry": "A0A087QKA0",
    "InterPro": "IPR001;IPR002;IPR003;IPR004;IPR005;IPR006;IPR007;",
    "Sequence": "MKVLWAAA"
  },
  {
    "Entry": "A0A087QKA1",
    "InterPro": "IPR001;IPR002;IPR003;IPR004;IPR005;",
    "Sequence": "MKVLWAAA"
  },
  {
    "Entry": "A0A087QKA2",
    "InterPro": "IPR001;IPR002;IPR003;IPR004;IPR005;IPR006;IPR007;IPR008;",
    "Sequence": "MKVLWAAA"
  }
]
```

> **Important:**
> The `InterPro` field **must end with a semicolon (`;`)**.

---

## Linux / Mac (curl)

```bash
curl -X POST http://localhost:50052/inject \
  -H "Content-Type: application/json" \
  -d '[
    {"Entry": "A0A087QH05", "InterPro": "IPR001;IPR002;IPR003;IPR004;IPR005;IPR006;IPR007;IPR008;IPR009;IPR010;", "Sequence": "MKVLWAAA"},
    {"Entry": "A0A087QKA0", "InterPro": "IPR001;IPR002;IPR003;IPR004;IPR005;IPR006;IPR007;", "Sequence": "MKVLWAAA"},
    {"Entry": "A0A087QKA1", "InterPro": "IPR001;IPR002;IPR003;IPR004;IPR005;", "Sequence": "MKVLWAAA"},
    {"Entry": "A0A087QKA2", "InterPro": "IPR001;IPR002;IPR003;IPR004;IPR005;IPR006;IPR007;IPR008;", "Sequence": "MKVLWAAA"}
  ]'
```

---

## Windows (PowerShell)

```powershell
$body = @(
    @{
        Entry = "A0A087QH05"
        InterPro = "IPR001;IPR002;IPR003;IPR004;IPR005;IPR006;IPR007;IPR008;IPR009;IPR010;"
        Sequence = "MKVLWAAA"
    },
    @{
        Entry = "A0A087QKA0"
        InterPro = "IPR001;IPR002;IPR003;IPR004;IPR005;IPR006;IPR007;"
        Sequence = "MKVLWAAA"
    },
    @{
        Entry = "A0A087QKA1"
        InterPro = "IPR001;IPR002;IPR003;IPR004;IPR005;"
        Sequence = "MKVLWAAA"
    },
    @{
        Entry = "A0A087QKA2"
        InterPro = "IPR001;IPR002;IPR003;IPR004;IPR005;IPR006;IPR007;IPR008;"
        Sequence = "MKVLWAAA"
    }
) | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:50052/inject -Method POST -Body $body -ContentType "application/json"
```

---

## View Results

### Print current state

```bash
curl http://localhost:50052/print
```

Or visit in browser:

```
http://localhost:50052/print
```

This returns:

* All proteins stored in memory
* Pairwise Jaccard similarity scores

---

## Health Check

```bash
curl http://localhost:50052/health
```

Example response:

```json
{
  "status": "healthy",
  "grpc_server": "running"
}
```

---

## What is Jaccard Similarity?

For two sets of InterPro domains **A** and **B**:

```
Jaccard(A, B) = |A ∩ B| / |A ∪ B|
```

* **0.0** → no shared domains
* **1.0** → identical domain sets

---

## Related Scripts

| Script           | Purpose                                |
| ---------------- | -------------------------------------- |
| `listener.py`    | FastAPI HTTP server (main entry point) |
| `server.py`      | gRPC backend (auto-started)            |
| `list-inject.py` | Injects proteins via gRPC              |
| `print.py`       | Prints stored proteins + correlations  |
| `send.py`        | Sends results to Neo4j                 |
| `file-import.py` | Loads proteins from file               |

---

## Authors

* **Andrea Tsilogiannis**
* **Robin Szymanski**
* **Alexandre Tinouert**

*University of Luxembourg — The Three Emperors*