import pandas as pd
from phishing.config import myclient
from phishing.logger import logging
from phishing.exception import PhishingException
import os,sys

def get_collection_as_dataframe(database_name:str, collection_name:str)->pd.DataFrame:
    """
    This Function import data from monoDB database and convert that data into pandas dataframe
    params:
    database_name
    collection_name
    """
    try:
        df = pd.DataFrame(list(myclient[database_name][collection_name].find(limit=1000)))
        logging.info(f"dataset found with rows and columns: {df.shape}")
        if '_id' in df.columns:
            df.drop('_id', axis=1, inplace=True)
        return df
    except Exception as e:
        PhishingException(e, sys)

get_collection_as_dataframe('phishing', 'dataset')