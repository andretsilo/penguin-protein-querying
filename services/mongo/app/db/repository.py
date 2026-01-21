from pymongo import MongoClient
from dotenv import load_dotenv
import os
from app.filters.filter import Filter
from app.model.protein import Protein
from app.config.logger import logger

load_dotenv()

uri = os.getenv("ATLAS_URI")
db_name = os.getenv("DB_NAME")
col_name = os.getenv("COL_NAME")

class ProteinRepository():
    def __init__(self, uri=uri, db_name=db_name, col_name=col_name):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[col_name]
    
    def drop(self):
        self.collection.drop()

    def import_many(self, data):
        self.collection.insert_many(data)
    
    def get(self, filter: Filter):
        return self.collection.find({"entry": {"$regex": filter.identifier, "$options": "i"}})
    
    def insert_one(self, protein: Protein):
        logger.info(f"Inserting entity: {protein}")
        self.collection.insert_one(dict(protein))
        


    
