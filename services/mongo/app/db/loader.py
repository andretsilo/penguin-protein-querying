from dotenv import dotenv_values
import csv
import requests
import gzip
import os
import shutil
from tqdm import tqdm
from app.config.logger import logger

config = dotenv_values(".env")
api_url = config["API_URL"]

path = "data/protein_penguin.tsv"

def download_url(url, stream=True, chunk_size=128):
    if not os.path.exists("data/"):
            os.makedirs("data/")

    r = requests.get(url, stream = True)
    with open(path + '.gz', 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)

def import_tsv(extract_path=path):
    try:
        logger.info("Starting download of objects.")
        download_url(api_url, path + ".gz")
        logger.info(f"{str(api_url)}")

        with gzip.open(path + ".gz", 'rb') as f_in:
            with open(path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        logger.info(f"Extracted file to: {extract_path}")
        raw_penguin_protein = csv.DictReader(open(path), delimiter="\t")
        return list(raw_penguin_protein)
    except Exception as e:
        logger.exception(f"Exception catched: {str(e)}")
        return None