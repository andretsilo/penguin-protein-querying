from pymongo import MongoClient
from dotenv import dotenv_values
import csv
import requests
import gzip
import shutil
from tqdm import tqdm
import os


### Environment and Global Variables ###

config = dotenv_values(".env")

uri = config["ATLAS_URI"]
db_name = config["DB_NAME"]
col_name = config["COL_NAME"]
api_url = config["API_URL"]

path0 = "penguin_protein"
path = "data/penguin_protein/penguin_protein.tsv"
path_root = "stream/data/penguin_protein/penguin_protein.tsv"


### Functions ###

def download_url(url, save_path):
    r = requests.get(url, stream=True)
    block_size = 1024
    total_size = int(r.headers.get("content-length", 0))
    with tqdm(total=total_size, unit="B", unit_scale=True) as progress_bar:
        with open(save_path, 'wb') as fd:
            for chunk in r.iter_content(block_size):
                fd.write(chunk)
                progress_bar.update(len(chunk))


def import_tsv(api_url, folder_path, tsv_path, tsv_gz_path):
        
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    ### Download, extract and unzip data ###
    download_url(api_url, tsv_gz_path)
    with gzip.open(tsv_gz_path, 'rb') as f_in:
        with open(tsv_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
            
    return csv.DictReader(open(tsv_path), delimiter="\t")
    

def import_main(api_url=api_url, path=path0, uri=uri, db_name=db_name, col_name=col_name):
    
    ### Setup paths and folders ###
    folder_path = f"data/{path}/"
    tsv_gz_path = f"data/{path}/{path}.tsv.gz"
    tsv_path = f"data/{path}/{path}.tsv"

    try:
        
        ### Setup MongoDB connection ###
        client = MongoClient(uri)
        db = client[db_name]
        collection = db[col_name]
        
        ### Remove current collection ###    
        collection.drop()
        print("Existing collection dropped. Starting download...")
        
        ### Download, extract and unzip data ###
        raw_protein = import_tsv(api_url, folder_path, tsv_path, tsv_gz_path)
        print(f"Correctly downloaded and extracted the file at {tsv_path}. Now importing to MongoDB...")
        
        ### Import data into MongoDB ###
        collection.insert_many(raw_protein)
        print("Import completed successfully.")
        
        return True
            
    except Exception as e:
        print(f"An error occurred: {e}")
        
        return False
    

### Main Execution ###

if  __name__ == "__main__":
    import_main()