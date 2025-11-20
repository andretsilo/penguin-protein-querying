from pymongo import MongoClient
from dotenv import dotenv_values
import csv
import requests
# import zipfile
import gzip
import shutil
from tqdm import tqdm

### Environment and Global Variables ###

config = dotenv_values(".env")

uri = config["ATLAS_URI"]
db_name = config["DB_NAME"]
col_name = config["COL_NAME"]
api_url = config["API_URL"]

path = "../../stream/data/protein_penguin.tsv"

client = MongoClient(uri)

db = client[db_name]
collection = db[col_name]

### Functions ###

def download_url(url, save_path, chunk_size=128):
    r = requests.get(url, stream=True)
    with open(save_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)


### Main Execution ###

if  __name__ == "__main__":
    
    try:
        collection.drop()
        print("Existing collection dropped. Starting download...")
        
        download_url(api_url, path + ".gz")
        
        with gzip.open(path + ".gz", 'rb') as f_in:
            with open(path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        print(f"Correctly downloaded and extracted the file at {path}. Now importing to MongoDB...")
        
        raw_penguin_protein = csv.DictReader(open(path), delimiter="\t")
        
        for row in tqdm(raw_penguin_protein):
            collection.insert_one(row)
            
        print("Import completed successfully.")
            
    except Exception as e:
        print(f"An error occurred: {e}")

