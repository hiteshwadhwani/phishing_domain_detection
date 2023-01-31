import pandas as pd
from phishing.config import myclient
from phishing.logger import logging
from phishing.exception import PhishingException
import os,sys
import numpy as np
import yaml
import pickle


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
        raise PhishingException(e, sys)

def save_numpy_array(file_path:str, array:np.array):
    try:
        file_dir = os.path.dirname(file_path)
        os.makedirs(file_dir, exist_ok=True)
        with open(file_path, 'wb') as file:
            np.save(file, array)
    except Exception as e:
        raise PhishingException(e, sys)

def load_numpy_arr(file_path:str):
    try:
        if not os.path.exists(file_path):
            raise Exception(f"file path {file_path} does not exists")
        with open(file_path, 'rb') as file:
            return np.load(file)
    except Exception as e:
        raise PhishingException(e, sys)

def save_object(file_path:str, object):
    try:
        file_dir = os.path.dirname(file_path)
        os.makedirs(file_dir, exist_ok=True)
        with open(file_path, 'wb') as f:
            pickle.dump(object, f)
    except Exception as e:
        raise PhishingException(e, sys)

def load_obj(file_path:str):
    try:
        if not os.path.exists(file_path):
            raise Exception(f"{file_path} file path does not exist")
        with open(file_path, 'rb') as file:
            return pickle.load(file)
    except Exception as e:
        raise PhishingException(e, sys)

def create_YAML_file(file_path:str, obj:dict):
    try:
        base_dir = os.path.dirname(file_path)
        os.makedirs(base_dir, exist_ok=True)

        with open(file_path, 'w') as file:
            yaml.dump(obj, file)
    except Exception as e:
        raise PhishingException(e, sys)
    
    
    