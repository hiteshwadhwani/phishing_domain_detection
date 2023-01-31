from dataclasses import dataclass
from datetime import datetime
import os,sys
from phishing.exception import PhishingException

ARTIFACT_DIR = os.path.join(os.getcwd(), 'artifact')
FEATURE_FILE_NAME = 'phishing.csv'
TEST_FILE_NAME = 'phishing_test.csv'
TRAIN_FILE_NAME = 'phishing_train.csv'
TRANSFORM_FILE_NAME = 'transform_obj.pkl'
MODEL_FILE_NAME = 'model.pkl'



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
    def __init__(self, training_pipeline_config:Training_pipeline_config):
        self.data_transformation_dir = os.path.join(training_pipeline_config.artifact_dir, 'data_transformation')
        self.data_transformation_obj_path = os.path.join(self.data_transformation_dir, 'transformer', TRANSFORM_FILE_NAME)
        self.train_file_path = os.path.join(self.data_transformation_dir, 'transformed_data', 'train_arr.npz')
        self.test_file_path = os.path.join(self.data_transformation_dir, 'transformed_data', 'test_arr.npz')
    def to_dict(self):
        return self.__dict__

class Data_validation_config:
    def __init__(self, training_pipeline_config:Training_pipeline_config):
        self.missing_values_threshold = 70
        self.data_validation_dir = os.path.join(training_pipeline_config.artifact_dir, 'data_validation')
        self.data_validation_report = os.path.join(self.data_validation_dir, 'data-validation-report.yaml')
    
    def to_dict(self):
        return self.__dict__

class Model_builder_config:
    def __init__(self, training_pipeline_config):
        self.model_builder_dir = os.path.join(training_pipeline_config.artifact_dir, 'model_builder')
        self.threshold_train_score = 0.5
        self.threshold_test_score = 0.5
        self.model_file_path = os.path.join(self.model_builder_dir, MODEL_FILE_NAME)

class Model_evaluation_config:
    def __init__(self):
        pass

class Model_pusher_config:
    def __init__(self, training_pipeline_config):
        self.model_pusher_dir = os.path.join(training_pipeline_config.artifact_dir, 'model_pusher', 'saved_models')
        self.model_pusher_model_path = os.path.join(self.model_pusher_dir, MODEL_FILE_NAME)
        self.model_pusher_transformer_path = os.path.join(self.model_pusher_dir, TRANSFORM_FILE_NAME)

