from fastapi import FastAPI
from dotenv import dotenv_values
from filters import filter as filter_router
from contextlib import asynccontextmanager
from neo4j import GraphDatabase

config = dotenv_values(".env")

@asynccontextmanager
async def lifespan(app: FastAPI):
    driver = GraphDatabase.driver(config["NEO4J_URI"],
                                  auth=(config["NEO4J_USER"], config["NEO4J_PASSWORD"]))
    driver.verify_connectivity()
    app.neo4j_driver = driver
    yield
    app.neo4j_driver.close()

app = FastAPI(lifespan=lifespan)

app.include_router(filter_router) #, tags=["books"], prefix="/book")