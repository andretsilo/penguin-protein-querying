from pydantic import BaseModel, Field

class Filter(BaseModel):
    identifier: str = Field(description = "Identifier for the protein to search for.")
