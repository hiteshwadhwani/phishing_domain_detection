import pymongo
from dataclasses import dataclass
from dotenv import load_dotenv
import os
from phishing.entity import config_entity
from phishing.component.data_ingestion import Data_ingestion
from phishing.component.data_transformation import Data_transformation
from phishing.component.data_validation import Data_validation
from phishing.exception import PhishingException
import os,sys

if __name__ == "__main__":
    try:

        # DATA INGESTION

        training_pipeline_config = config_entity.Training_pipeline_config()
        print(training_pipeline_config.to_dict())
        data_ingestion_config = config_entity.Data_ingestion_config(training_pipeline_config=training_pipeline_config)
        print(data_ingestion_config.to_dict())
        data_ingestion = Data_ingestion(data_ingestion_config)
        data_ingestion_artifact = data_ingestion.intiate_data_ingestion()

        # DATA TRANSFORMATION

        data_transformation_config = config_entity.Data_transformation_config(training_pipeline_config=training_pipeline_config)
        data_transformation_obj = Data_transformation(data_transformation_config=data_transformation_config,
        data_ingestion_artifact=data_ingestion_artifact)
        data_transformation_artifact = data_transformation_obj.intiate_data_transformation()
        print(data_transformation_artifact)

        # DATA VALIDATION

        data_validation_config = config_entity.Data_validation_config(training_pipeline_config=training_pipeline_config)
        data_validation_obj = Data_validation(data_validation_config=data_validation_config,
        data_ingestion_artifact=data_ingestion_artifact)
        data_validation_artifact = data_validation_obj.intiate_data_validaiton()
        print(data_validation_artifact)


    except Exception as e:
        raise PhishingException(e,sys)