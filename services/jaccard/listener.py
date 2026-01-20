from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List
import subprocess
import json
import sys
import threading
import time

app = FastAPI(
    title="Protein Data Injection API",
    description="""
    ## Overview
    HTTP interface for managing protein data and calculating Jaccard similarity coefficients via gRPC.
    
    ## Features
    - Inject protein data with InterPro domain annotations (and automatically sent to Neo4j)
    - Calculate Jaccard similarity between all protein pairs (automatic)
    - View current state and correlations (print, state not supported via request for confidentiality reasons)
    
    ## Workflow
    1. POST protein data to `/inject` endpoint
    2. Data is processed by gRPC server (auto-started)
    3. Jaccard similarities calculated for all pairs
    4. View results using `/print` endpoint
    5. Data can be forwarded to Neo4j (optional)
    
    ## Jaccard Similarity
    Measures how similar two sets are: `Jaccard(A, B) = |A ∩ B| / |A ∪ B|`
    
    Score ranges from 0.0 (no similarity) to 1.0 (identical sets)
    """,
    version="1.0.0",
    contact={
        "name": "Andrea Tsilogiannis, Robin Szymanski, Alexandre Tinouert"
    },
    license_info={
        "name": "University of Luxembourg - The Three Emperors",
    }
)

# Global variable to track server process
grpc_server_process = None

class Protein(BaseModel):
    Entry: str = Field(
        ..., 
        description="Unique protein entry identifier",
        example="A0A087QH05"
    )
    InterPro: str = Field(
        ..., 
        description="Semicolon-separated list of InterPro domain IDs (must end with semicolon)",
        example="IPR001;IPR002;IPR003;"
    )
    Sequence: str = Field(
        ..., 
        description="Amino acid sequence",
        example="MKVLWAALLVTFLAGCQAK"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "Entry": "A0A087QH05",
                "InterPro": "IPR001;IPR002;IPR003;IPR004;IPR005;",
                "Sequence": "MKVLWAALLVTFLAGCQAKVEQAVETEPEPELRQQTEWQ"
            }
        }

class InjectionResponse(BaseModel):
    status: str = Field(..., description="Status of the operation", example="success")
    message: str = Field(..., description="Human-readable message", example="Data injected successfully")
    proteins_count: int = Field(..., description="Number of proteins processed", example=4)
    script_output: str = Field(..., description="Output from the injection script", example="Added 4 proteins.")

class ErrorResponse(BaseModel):
    status: str = Field(..., example="error")
    message: str = Field(..., example="Script execution failed")
    error: str = Field(None, example="Connection refused")

class PrintResponse(BaseModel):
    status: str = Field(..., description="Status of the operation", example="success")
    output: str = Field(
        ..., 
        description="Formatted output showing all proteins and their Jaccard correlations",
        example="[1] A0A087QH05\n    Correlations: 3 pairs\n      - A0A087QKA0: 0.7000\n      - A0A087QKA1: 0.5000\n      - A0A087QKA2: 0.8000"
    )

class HealthResponse(BaseModel):
    status: str = Field(..., example="healthy")
    grpc_server: str = Field(..., example="running")

def start_grpc_server():
    """Start the gRPC server in a background process."""
    global grpc_server_process
    try:
        grpc_server_process = subprocess.Popen(
            [sys.executable, 'server.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        # Give it a moment to start
        time.sleep(2)
        print("✓ gRPC Server started successfully on port 50051")
        return True
    except Exception as e:
        print(f"✗ Failed to start gRPC server: {e}")
        return False

@app.post(
    "/inject", 
    response_model=InjectionResponse,
    responses={
        200: {
            "description": "Data injected successfully",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "message": "Data injected successfully",
                        "proteins_count": 4,
                        "script_output": "Added 4 proteins."
                    }
                }
            }
        },
        422: {
            "description": "Validation Error - Missing or invalid fields",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body", 0, "Sequence"],
                                "msg": "field required",
                                "type": "value_error.missing"
                            }
                        ]
                    }
                }
            }
        },
        500: {
            "description": "Server Error - Script execution failed",
            "model": ErrorResponse
        },
        504: {
            "description": "Timeout - Script execution timed out"
        }
    },
    tags=["Protein Data"],
    summary="Inject protein data into gRPC server"
)
async def inject_proteins(proteins: List[Protein]):
    """
    ## Inject Protein Data
    
    Receives a list of proteins and injects them into the gRPC server for processing.
    
    ### Process Flow:
    1. Validates protein data structure
    2. Sends data to gRPC server via `list-inject.py`
    3. Calculates Jaccard similarities between all protein pairs
    4. Automatically forwards results via `send.py`
    
    ### Expected Payload:
    ```json
    [
        {
            "Entry": "A0A087QH05",
            "InterPro": "IPR001;IPR002;IPR003;",
            "Sequence": "MKVLWAALLVT..."
        }
    ]
    ```
    
    ### Notes:
    - InterPro field must end with a semicolon
    - Multiple proteins will be compared pairwise
    - Results can be viewed via `/print` endpoint
    """
    try:
        # Convert Pydantic models to dict for JSON serialization
        payload = [protein.model_dump() for protein in proteins]
        
        # Convert payload to JSON string for command line argument
        payload_json = json.dumps(payload)
        
        # Run list-inject.py with the payload
        result = subprocess.run(
            [sys.executable, 'list-inject.py', payload_json],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        print("Data collected. Now running send.py to forward data via HTTP POST...")
        
        sending = subprocess.run(
            [sys.executable, 'send.py'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        print(sending)
        
        # Check if the script executed successfully
        if result.returncode == 0:
            return InjectionResponse(
                status="success",
                message="Data injected successfully",
                proteins_count=len(payload),
                script_output=result.stdout
            )
        else:
            raise HTTPException(
                status_code=500,
                detail={
                    "status": "error",
                    "message": "Script execution failed",
                    "error": result.stderr
                }
            )
            
    except subprocess.TimeoutExpired:
        raise HTTPException(
            status_code=504,
            detail={
                "status": "error",
                "message": "Script execution timed out"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "message": str(e)
            }
        )

@app.get(
    "/print", 
    response_model=PrintResponse,
    responses={
        200: {
            "description": "Successfully retrieved current state",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "output": "[1] A0A087QH05\n    Correlations: 3 pairs (excluding self)\n      - A0A087QKA0: 0.7000\n      - A0A087QKA1: 0.5000\n      - A0A087QKA2: 0.8000\n\nSummary: 4 proteins, avg 3.0 correlations per protein"
                    }
                }
            }
        },
        500: {"description": "Script execution failed"},
        504: {"description": "Script execution timed out"}
    },
    tags=["Protein Data"],
    summary="View current state and correlations"
)
async def print_current_state():
    """
    ## View Current State
    
    Executes `print.py` to retrieve and display all proteins with their Jaccard correlations.
    
    ### Output Includes:
    - List of all proteins in the system
    - Jaccard similarity scores for each protein pair
    - Summary statistics (total proteins, average correlations)
    
    ### Example Output:
    ```
    [1] A0A087QH05
        Correlations: 3 pairs (excluding self)
          - A0A087QKA0: 0.7000
          - A0A087QKA1: 0.5000
          - A0A087QKA2: 0.8000
    
    Summary: 4 proteins, avg 3.0 correlations per protein
    ```
    
    The output is returned both as HTTP response and printed to the server console.
    """
    try:
        print("\n" + "="*60)
        print("Executing print.py to view current state...")
        print("="*60)
        
        result = subprocess.run(
            [sys.executable, 'print.py'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Print to console
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        print("="*60 + "\n")
        
        if result.returncode == 0:
            return PrintResponse(
                status="success",
                output=result.stdout
            )
        else:
            raise HTTPException(
                status_code=500,
                detail={
                    "status": "error",
                    "message": "print.py execution failed",
                    "error": result.stderr
                }
            )
            
    except subprocess.TimeoutExpired:
        raise HTTPException(
            status_code=504,
            detail={
                "status": "error",
                "message": "print.py execution timed out"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "message": str(e)
            }
        )

@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["System"],
    summary="Health check endpoint"
)
async def health_check():
    """
    ## Health Check
    
    Returns the health status of both the FastAPI listener and the gRPC server.
    
    ### Response:
    - `status`: Overall health status ("healthy" or "unhealthy")
    - `grpc_server`: Status of the gRPC server ("running" or "not running")
    """
    return {
        "status": "healthy",
        "grpc_server": "running" if grpc_server_process and grpc_server_process.poll() is None else "not running"
    }

@app.get(
    "/",
    tags=["Documentation"],
    summary="API information and quick start"
)
async def root():
    """
    ## Root Endpoint
    
    Provides comprehensive API information including:
    - Server details and ports
    - Complete workflow description
    - All available endpoints with examples
    - Quick start guide
    """
    return {
        "title": "Protein Data Injection API",
        "description": "HTTP interface for managing protein data and Jaccard similarity calculations via gRPC",
        "version": "1.0.0",
        "servers": {
            "fastapi_listener": "http://localhost:50052",
            "grpc_server": "localhost:50051"
        },
        "workflow": {
            "1": "Start this listener (which auto-starts the gRPC server)",
            "2": "POST protein data to /inject endpoint",
            "3": "Data is sent to gRPC server for processing",
            "4": "Jaccard similarities are calculated between all protein pairs",
            "5": "Use /print to view current state and correlations",
            "6": "Data can be forwarded to Neo4j service via send.py"
        },
        "endpoints": {
            "POST /inject": {
                "description": "Inject protein data into gRPC server",
                "payload": "Array of protein objects with Entry, InterPro, and Sequence fields",
                "example": [
                    {
                        "Entry": "PROT_001",
                        "InterPro": "IPR001;IPR002;IPR003;",
                        "Sequence": "MKVLW..."
                    }
                ]
            },
            "GET /print": {
                "description": "View current state of all proteins and their Jaccard correlations",
                "returns": "Formatted output showing proteins and their similarity scores"
            },
            "GET /health": {
                "description": "Check health status of both FastAPI and gRPC servers"
            },
            "GET /help": {
                "description": "Detailed usage instructions and examples"
            },
            "GET /docs": {
                "description": "Interactive Swagger API documentation"
            }
        },
        "quick_start": "Visit /help for detailed examples or /docs for interactive documentation"
    }

@app.get(
    "/help",
    tags=["Documentation"],
    summary="Detailed usage guide and examples"
)
async def help_endpoint():
    """
    ## Comprehensive Help Documentation
    
    Provides detailed information about:
    - API architecture and workflow
    - Jaccard similarity explanation with examples
    - Usage examples for Linux, Mac, and Windows
    - Data format specifications
    - Response format details
    - Tips and best practices
    """
    return {
        "title": "Protein Data Injection API - Help & Usage Guide",
        "overview": {
            "description": "This API manages protein data and calculates Jaccard similarity coefficients between proteins based on their InterPro domain annotations.",
            "architecture": [
                "FastAPI listener (this service) on port 50052",
                "gRPC server (server.py) on port 50051",
                "Both services start automatically when you run listener.py"
            ]
        },
        "what_is_jaccard_similarity": {
            "description": "Jaccard similarity measures how similar two sets are",
            "formula": "Jaccard(A, B) = |A ∩ B| / |A ∪ B|",
            "example": {
                "protein_A_domains": ["IPR001", "IPR002", "IPR003"],
                "protein_B_domains": ["IPR001", "IPR002", "IPR005"],
                "intersection": ["IPR001", "IPR002"],
                "union": ["IPR001", "IPR002", "IPR003", "IPR005"],
                "jaccard_score": "2/4 = 0.5"
            }
        },
        "usage_examples": {
            "1_inject_data_curl": {
                "description": "Inject protein data using curl (Linux/Mac)",
                "command": """curl -X POST http://localhost:50052/inject \\
  -H "Content-Type: application/json" \\
  -d '[
    {"Entry": "PROT_001", "InterPro": "IPR001;IPR002;IPR003;", "Sequence": "MKVLW..."},
    {"Entry": "PROT_002", "InterPro": "IPR001;IPR002;", "Sequence": "MAKTP..."}
  ]'"""
            },
            "2_inject_data_powershell": {
                "description": "Inject protein data using PowerShell (Windows)",
                "command": """$body = @(
    @{Entry = "PROT_001"; InterPro = "IPR001;IPR002;IPR003;"; Sequence = "MKVLW..."},
    @{Entry = "PROT_002"; InterPro = "IPR001;IPR002;"; Sequence = "MAKTP..."}
) | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:50052/inject -Method POST -Body $body -ContentType "application/json\""""
            },
            "3_view_current_state": {
                "description": "View all proteins and their correlations",
                "curl": "curl http://localhost:50052/print",
                "browser": "Open http://localhost:50052/print in your browser"
            },
            "4_check_health": {
                "description": "Check if both servers are running",
                "curl": "curl http://localhost:50052/health"
            }
        },
        "data_format": {
            "protein_object": {
                "Entry": "Unique protein identifier (string)",
                "InterPro": "Semicolon-separated list of InterPro domain IDs (e.g., 'IPR001;IPR002;')",
                "Sequence": "Amino acid sequence (string)"
            },
            "note": "InterPro field should end with a semicolon for proper parsing"
        },
        "workflow_details": {
            "step_1": "POST protein data to /inject",
            "step_2": "listener.py calls list-inject.py to send data to gRPC server",
            "step_3": "gRPC server processes proteins and extracts InterPro domains",
            "step_4": "Server calculates Jaccard similarity for all protein pairs",
            "step_5": "listener.py automatically calls send.py to forward results",
            "step_6": "Use /print to view current state and all correlations",
            "optional": "Results can be sent to Neo4j service at localhost:8080/api/proteins"
        },
        "response_formats": {
            "injection_success": {
                "status": "success",
                "message": "Data injected successfully",
                "proteins_count": 2,
                "script_output": "Server response..."
            },
            "print_output_format": {
                "status": "success",
                "output": "[1] PROT_001\n    Correlations: 1 pairs\n      - PROT_002: 0.6667\n..."
            }
        },
        "additional_scripts": {
            "print.py": "View current state (also available via GET /print)",
            "send.py": "Send results to Neo4j (called automatically after injection)",
            "file-import.py": "Import from file (run directly)",
            "list-inject.py": "Inject from command line (called by /inject endpoint)"
        },
        "tips": [
            "Use /docs for interactive API testing",
            "The gRPC server maintains state across requests",
            "Correlations are cached for performance",
            "Each protein is compared with all others (excluding itself)",
            "Results show Jaccard scores from 0.0 (no similarity) to 1.0 (identical)"
        ]
    }

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up gRPC server process on shutdown"""
    global grpc_server_process
    if grpc_server_process:
        print("\nShutting down gRPC server...")
        grpc_server_process.terminate()
        grpc_server_process.wait()

if __name__ == '__main__':
    import uvicorn
    
    print("\n" + "="*70)
    print("  PROTEIN DATA INJECTION API - STARTUP")
    print("="*70)
    
    # Start gRPC server first
    print("\n[1/2] Starting gRPC Server (server.py)...")
    if start_grpc_server():
        print("      → gRPC Server: Running on localhost:50051")
    else:
        print("      → WARNING: gRPC Server failed to start")
        print("      → You may need to start server.py manually")
    
    # Start FastAPI listener
    print("\n[2/2] Starting FastAPI Listener...")
    print("      → FastAPI Listener: http://0.0.0.0:50052")
    print("\n" + "="*70)
    print("  BOTH SERVICES RUNNING")
    print("="*70)
    print("\n📍 API Endpoints:")
    print("   • POST http://localhost:50052/inject    - Inject protein data")
    print("   • GET  http://localhost:50052/print     - View current state")
    print("   • GET  http://localhost:50052/health    - Health check")
    print("   • GET  http://localhost:50052/help      - Detailed help")
    print("   • GET  http://localhost:50052/docs      - Interactive API docs")
    print("\n" + "="*70 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=50052)