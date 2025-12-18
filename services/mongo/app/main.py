from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from app.filters.filter import Filter
from pymongo import MongoClient
from app.model.protein import Protein
from dotenv import dotenv_values
from app.config.logger import logger
from app.db.loader import import_tsv
from app.db.repository import ProteinRepository
from starlette.responses import JSONResponse

config = dotenv_values(".env")
repository = ProteinRepository()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Import the data
    data = import_tsv()

    # Create a list of proteins according to the protein class
    proteins = []
    for row in data:
        protein = Protein(
            entry=row["Entry"],
            reviewed=row["Reviewed"],
            entry_name=row["Entry Name"],
            protein_name=row["Protein names"],
            gene_name=row["Gene Names"],
            organism=row["Organism"],
            interpro=row["InterPro"],
            ec_number=row["EC number"],
            sequence=row["Sequence"]
        )
        proteins.append(protein)

    # Start the mongoDB client
    mongodb_client = MongoClient(config["ATLAS_URI"])
    database = mongodb_client[config["DB_NAME"]]
    collection = database[config["COL_NAME"]]

    # For MongoDB, the results must be in a model_dump (dict deprecated). insert_many is much faster than insert_one.
    collection.insert_many([p.model_dump() for p in proteins])
    yield

app = FastAPI(lifespan = lifespan)

@app.get("/protein/")
async def getProtein(filter: Filter):
    return JSONResponse(content=str(list(repository.get(filter))))

@app.post("/protein/")
async def insertProtein(protein: Protein):
    try:
        repository.insert_one(protein)
        return {"message": "Data inserted correctly"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Something went fucking wrong.")