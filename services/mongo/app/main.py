from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from app.filters.filter import Filter
from pymongo import MongoClient
from app.model.protein import Protein
from dotenv import load_dotenv
import os
from app.config.logger import logger
from app.db.loader import import_tsv
from app.db.repository import ProteinRepository
from app.db.statistics import StatisticsRepository
from starlette.responses import JSONResponse
from pymongo.errors import PyMongoError

load_dotenv()
mongodb_client = MongoClient(os.getenv("ATLAS_URI"))
database = mongodb_client[os.getenv("DB_NAME")]
collection = database[os.getenv("COL_NAME")]

repository = ProteinRepository()
statistics_mongo = StatisticsRepository(collection)

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

    # For MongoDB, the results must be in a model_dump (dict deprecated). insert_many is much faster than insert_one.
    collection.insert_many([p.model_dump() for p in proteins])
    yield

app = FastAPI(lifespan = lifespan)

@app.get("/health")
async def health_check():
    status = {"api": "healthy", "mongodb": "unknown"} # Default status
    try:
        client = MongoClient(os.getenv("ATLAS_URI"),
                             serverSelectionTimeoutMS=2000)    # Wait for 2s
        client.admin.command("ping")
        status["mongodb"] = "healthy"
    except PyMongoError:
        status["mongodb"] = "unreachable"
    return status

@app.get("/protein/")
async def getProtein(filter: Filter):
    proteins = list(repository.get(filter))
    for protein in proteins:
        protein["_id"] = str(protein["_id"])
    return proteins

@app.post("/protein/")
async def insertProtein(protein: Protein):
    try:
        repository.insert_one(protein)
        return {"message": "Data inserted correctly"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Something went fucking wrong.")

@app.get("/stats-annotation-coverage")
async def annotation_coverage():
    return statistics_mongo.annotation_coverage()

@app.get("/stats-interpro-group-size")
async def interpro_group_size():
    return statistics_mongo.interpro_group_size()

@app.get("/stats-ec-group-size")
async def ec_group_size():
    return statistics_mongo.ec_group_size()

@app.get("/stats-ec-group-size")
async def sequence_length():
    return statistics_mongo.sequence_length()