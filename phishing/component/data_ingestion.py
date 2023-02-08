import pandas as pd
import numpy as np
from phishing.entity import config_entity, artifact_entity
from phishing.logger import logging
from phishing.exception import PhishingException
from sklearn.model_selection import train_test_split
from phishing import utils
import os,sys


class Data_ingestion:
    def __init__(self, data_ingestion_config:config_entity.Data_ingestion_config):
        logging.info(f"{5 * '<<'} DATA INGESTION {5 * '>>'}")
        self.data_ingestion_config = data_ingestion_config

    def intiate_data_ingestion(self):
        try:
            logging.info("Importing dataset")
            df = utils.get_collection_as_dataframe(database_name=self.data_ingestion_config.database_name, collection_name=self.data_ingestion_config.collection_name)
            print(f"df:{df.shape}")

            logging.info(f"replacing na values {df.isna().sum()} to np.NAN dtype")     
            df.replace(to_replace='na', value=np.NAN, inplace=True)

            feature_store_dir = os.path.dirname(self.data_ingestion_config.feature_file_path)
            os.makedirs(feature_store_dir, exist_ok=True)

            logging.info(f"saving dataset to folder {self.data_ingestion_config.feature_file_path}")
            df.to_csv(path_or_buf=self.data_ingestion_config.feature_file_path, index=False, header=True)

            dataset_dir = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dataset_dir, exist_ok=True)

        
            logging.info("spitting data in train and test")
            train_df, test_df = train_test_split(df, test_size=self.data_ingestion_config.test_size, random_state=42)
            logging.info(f"train_df shape: {train_df.shape}, test_df shape:{test_df.shape}")

            logging.info(f"saving train and test dataset to path {self.data_ingestion_config.train_file_path}")
            train_df.to_csv(self.data_ingestion_config.train_file_path, index=False, header=True)
            test_df.to_csv(self.data_ingestion_config.test_file_path, index=False, header=True)


            data_ingestion_artifact = artifact_entity.Data_ingestion_artifact(feature_store_path=self.data_ingestion_config.feature_file_path,
            train_file_path=self.data_ingestion_config.train_file_path,
            test_file_path=self.data_ingestion_config.test_file_path)
            logging.info(f"============DATA INGESTION ARTIFACT============ : {data_ingestion_artifact}")

            return data_ingestion_artifact
        except Exception as e:
            raise PhishingException(e, sys)
        

