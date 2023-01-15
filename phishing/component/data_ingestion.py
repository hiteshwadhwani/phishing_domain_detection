import pandas as pd
import numpy as np
from phishing.entity import config_entity, artifact_entity
from phishing.logger import logging
from phishing.exception import PhishingException
from sklearn.model_selection import train_test_split


class Data_ingestion:
    def __init__(self, data_ingestion_config:config_entity.Data_ingestion_config):
        logging.info(f"{2 * '<<'} DATA INGESTION {2 * '>>'}")
        self.data_ingestion_config = data_ingestion_config

    def intiate_data_ingestion():
        pass