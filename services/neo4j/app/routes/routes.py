from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder

from ..model.protein import Protein

router = APIRouter()


@router.post("/", response_description="Create a new book", status_code=status.HTTP_201_CREATED, response_model=Book)
def create_book(request: Request, protein: Protein = Body(...)):
    driver = request.app.neo4j_driver

    summary = driver.execute_query("""
        CREATE (a:Person {name: $name})
        CREATE (b:Person {name: $friendName})
        CREATE (a)-[:KNOWS]->(b)
        """,
                                   name="Alice", friendName="David",
                                   database_="<database-name>",
                                   ).summary
    print("Created {nodes_created} nodes in {time} ms.".format(
        nodes_created=summary.counters.nodes_created,
        time=summary.result_available_after
    ))

    return summary

# ID or name or description
@router.get("/", response_description="Get a protein by ID, name or description", response_model=Protein)
async def find_protein(identifier: str, request: Request, description: str = None):

    # Try ID lookup
    book = request.app.database["books"].find_one({"_id": identifier})
    if book:
        return book

    # Try name lookup
    book = request.app.database["books"].find_one({"name": identifier})
    if book:
        return book

    # Try description lookup
    if description is not None:
        book = request.app.database["books"].find_one({"age": description})
        if book:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {id} not found")





