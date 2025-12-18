from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
import subprocess
import json
import sys

app = FastAPI(
    title="Protein Data Injection API",
    description="HTTP listener for injecting protein data into gRPC server",
    version="1.0.0"
)

class Protein(BaseModel):
    Entry: str = Field(..., description="Protein entry identifier")
    InterPro: str = Field(..., description="InterPro domains (semicolon-separated)")
    Sequence: str = Field(..., description="Protein sequence")

class InjectionResponse(BaseModel):
    status: str
    message: str
    proteins_count: int
    script_output: str

class ErrorResponse(BaseModel):
    status: str
    message: str
    error: str = None

@app.post("/inject", response_model=InjectionResponse)
async def inject_proteins(proteins: List[Protein]):
    """
    Receives a POST request with protein data and injects it into the gRPC server.
    
    Expected JSON payload:
    [
        { "Entry": "HTTP_PROT_01", "InterPro": "IPR001;IPR002;IPR003;", "Sequence": "MKV..." },
        { "Entry": "HTTP_PROT_02", "InterPro": "IPR001;IPR002;", "Sequence": "MKV..." },
        ...
    ]
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
        
        print("Now running send.py to forward data via HTTP POST...")
        
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

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Protein Data Injection API",
        "endpoints": {
            "POST /inject": "Inject protein data into gRPC server",
            "GET /health": "Health check",
            "GET /docs": "Interactive API documentation",
            "GET /redoc": "Alternative API documentation"
        }
    }

if __name__ == '__main__':
    import uvicorn
    print("Starting FastAPI listener on http://0.0.0.0:50052")
    print("POST protein data to http://localhost:50052/inject")
    print("View interactive docs at http://localhost:50052/docs")
    uvicorn.run(app, host="0.0.0.0", port=50052)