import pymongo
from dataclasses import dataclass
from dotenv import load_dotenv
import os
from phishing.entity import config_entity
from phishing.component.data_ingestion import Data_ingestion
from phishing.exception import PhishingException
import os,sys

if __name__ == "__main__":
    try:
        training_pipeline_config = config_entity.Training_pipeline_config()
        print(training_pipeline_config.to_dict())
        data_ingestion_config = config_entity.Data_ingestion_config(training_pipeline_config=training_pipeline_config)
        print(data_ingestion_config.to_dict())
        data_ingestion = Data_ingestion(data_ingestion_config)
        print(data_ingestion.intiate_data_ingestion())

    except Exception as e:
        PhishingException(e,sys)