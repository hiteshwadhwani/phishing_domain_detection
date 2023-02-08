from phishing.logger import logging
from phishing.exception import PhishingException
import os,sys
from phishing.entity import config_entity, artifact_entity
import pandas as pd
from xgboost import XGBClassifier
from phishing.utils import load_numpy_arr, save_object
from sklearn.metrics import f1_score

class Model_builder:
    def __init__(self, model_builder_config, data_transformation_artifact):
        logging.info(f'{2 * "<<"} MODEL BUILDER {2 * ">>"}')
        self.model_builder_config = model_builder_config
        self.data_transformation_artifact = data_transformation_artifact
    
    def model_builder(self, X_train, y_train):
        try:
            xg_model = XGBClassifier()
            xg_model.fit(X_train, y_train)
            return xg_model
        except Exception as e:
            raise PhishingException(e, sys)
        
    def hyperparameter_model(self):
        pass
    
    def intiate_model_builder(self):
        try:
            logging.info('Loading transformed train and test array')
            train_arr = load_numpy_arr(file_path=self.data_transformation_artifact.train_file_path)
            test_arr = load_numpy_arr(file_path=self.data_transformation_artifact.test_file_path)
            logging.info(f'transformed train array: {train_arr.shape}, transformed test array shape {test_arr.shape}')

            X_train, y_train = train_arr[:, :-1],  train_arr[:, -1]
            X_test, y_test = test_arr[:, :-1], test_arr[:, -1]

            logging.info('Training model on train dataset')
            ml_model = self.model_builder(X_train, y_train) 

            train_predict = ml_model.predict(X_train)
            train_score = f1_score(train_predict, y_train)
            logging.info(f'training score : {train_score}')

            test_predict = ml_model.predict(X_test)
            test_score = f1_score(y_test, test_predict)
            logging.info(f'testing score : {test_score}')

            if train_score < self.model_builder_config.threshold_train_score:
                raise Exception("model does not performed well on training dataset")

            if test_score < self.model_builder_config.threshold_test_score:
                raise Exception("Model does not performed well on testing dataset")

            save_object(file_path=self.model_builder_config.model_file_path, object=ml_model)

            model_builder_artifact = artifact_entity.Model_builder_artifact(model_path=self.model_builder_config.model_file_path,
            train_score=train_score, test_score=test_score)

            logging.info(f"================MODEL TRAINING ARTIACT============== : {model_builder_artifact}")

            return model_builder_artifact
        except Exception as e:
            raise PhishingException(e, sys)