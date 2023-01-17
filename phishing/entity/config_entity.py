from dataclasses import dataclass
from datetime import datetime
import os,sys
from phishing.exception import PhishingException

ARTIFACT_DIR = os.path.join(os.getcwd(), 'artifact')
FEATURE_FILE_NAME = 'phishing.csv'
TEST_FILE_NAME = 'phishing_test.csv'
TRAIN_FILE_NAME = 'phishing_train.csv'

class Training_pipeline_config:
    def __init__(self):
        try:
            self.artifact_dir = os.path.join(ARTIFACT_DIR,  f"{datetime.now().strftime('%m:%d:%Y__%H:%M:%S')}")
        except Exception as e:
            PhishingException(e, sys)
    def to_dict(self):
        return self.__dict__

class Data_ingestion_config:
    def __init__(self, training_pipeline_config:Training_pipeline_config):
        try:
            self.collection_name = 'dataset'
            self.database_name = 'phishing'
            self.test_size = 0.2
            self.data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir, 'data_ingestion')
            self.feature_file_path = os.path.join(self.data_ingestion_dir, 'feature_store', FEATURE_FILE_NAME)
            self.train_file_path = os.path.join(self.data_ingestion_dir, 'dataset', TRAIN_FILE_NAME)
            self.test_file_path = os.path.join(self.data_ingestion_dir, 'dataset', TEST_FILE_NAME)
        except Exception as e:
            PhishingException(e, sys)
    def to_dict(self):
        return self.__dict__
        

class Data_transformation_config:
    pass

class Data_validation_config:
    pass

class Model_builder_config:
    pass

class Model_evaluation_config:
    pass

class Model_pusher_config:
    pass

