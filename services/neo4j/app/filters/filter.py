from pydantic import BaseModel, Field

class Filter(BaseModel):
    identifier: str = Field(description = "Identifier for the protein to search for.")
    name: str = Field(description = "Name of the protein to search for.")
    description: str = Field(description = "Description of the protein to search for.")