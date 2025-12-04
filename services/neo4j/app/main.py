from fastapi import FastAPI
from dotenv import dotenv_values
from routes.routes import router
#from filters.filter import Filter
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

app.include_rounter(router)
#app.include_router(Filter) #, tags=["books"], prefix="/book")