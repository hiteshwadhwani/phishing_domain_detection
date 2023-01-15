import pandas as pd
import numpy as np
from dotenv import load_dotenv
import os,sys
import pymongo
import json

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

myclient = pymongo.MongoClient(MONGO_DB_URL)
print(myclient)

DATABASE_NAME = "phishing"
COLLECTION_NAME = "dataset"

db = myclient[DATABASE_NAME]
col = db[COLLECTION_NAME]


def dump_data_in_mongodb():
    """This function will save all your data in mongoDB database
    ============================================================
    params:
    database: Name of your database
    collection : Name of your collection
    """
    url = 'https://drive.google.com/file/d/1zwUKSiaEM43A875jAUmqCKQ3ooxo8XIS/view?usp=share_link'
    url = url='https://drive.google.com/uc?id=' + url.split('/')[-2]
    df = pd.read_csv(url)

    print("Rows and columns in dataset", df.shape)

    json_records = list(json.loads(df.T.to_json()).values())

    col.insert_many(json_records)


if __name__ == "__main__":
    dump_data_in_mongodb()
