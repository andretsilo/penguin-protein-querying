from pydantic import BaseModel, Field
from enum import StrEnum

class ReviewedEnum(StrEnum):
    reviewed = "reviewed",
    unreviewed = "unreviewed"

class Protein(BaseModel):
    entry: str = Field(description = "Identifier for the protein entry.")
    reviewed: ReviewedEnum = Field(description = "Whether the protein has been reviewed or not.")
    entry_name: str = Field(description = "Name for the identifier.")
    protein_name: str = Field(description = "The protein name.")
    gene_name: str = Field(description = "The gene name that is related to the protein.")
    organism: str = Field(description = "The organism of origin.")
    interpro: str = Field(description = "Sequence")
    ec_number: str = Field(description = "Domain of correlation for the protein")
    sequence: str = Field(description = "Sequence of amminoacids")