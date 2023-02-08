from phishing.logger import logging
from phishing.exception import PhishingException
import os,sys
from phishing.entity import config_entity, artifact_entity
from phishing.utils import load_obj
import pandas as pd
from phishing.predictor import ModelResolver
from phishing.config import TARGET_FEATURE
from sklearn.metrics import f1_score

class Model_evaluation:
    def __init__(self,data_transformation_artifact:artifact_entity.Data_transformation_artifact,
                model_builder_artifact:artifact_entity.Model_builder_artifact,
                data_ingestion_artifact:artifact_entity.Data_ingestion_artifact):
        logging.info(f"{5 * '<<'} MODEL EVALUATION {5 * '>>'}")
        self.data_transformation_artifact = data_transformation_artifact
        self.model_builder_artifact = model_builder_artifact
        self.data_ingestion_artifact =data_ingestion_artifact
        self.model_resolver = ModelResolver(model_registory='saved_models', 
                                            transformer_dir_name='transformer',
                                            model_dir_name='model')
    def intiate_model_evaluation(self):
        try:
            logging.info('Getting latest directory from saved folder')
            latest_dir = self.model_resolver.get_latest_dir_path()
            if latest_dir is None:
                logging.info('No save model found')
                model_evaluation_artifact = artifact_entity.Model_evaluation_artifact(model_accepted=True, improved_accuracy=None)
                logging.info(f'Model_evaluation_artifact : {model_evaluation_artifact}')
                return model_evaluation_artifact

            # Import dataset
            logging.info('Import dataset for testing previous trained model and current model')
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            y_test = test_df[TARGET_FEATURE]
            X_test = test_df.drop(TARGET_FEATURE, axis=1)

            
            # Import current trained model and transformer from artifact folder
            logging.info(f'Importing current model from path : {self.model_builder_artifact.model_path}')
            curr_model = load_obj(file_path=self.model_builder_artifact.model_path)

            logging.info(f'Importing current transformer from path : {self.data_transformation_artifact.transform_obj_file_path}')
            curr_transformer = load_obj(file_path=self.data_transformation_artifact.transform_obj_file_path)

            input_features = list(curr_transformer.feature_names_in_)
            input_array = curr_transformer.transform(X_test[input_features])
            curr_model_pred =  curr_model.predict(input_array)

            curr_model_score = f1_score(curr_model_pred, y_test)
            logging.info(f'f1_score of currently trained model : {curr_model_score}')


        
            # import previous trained model and transformer from saved_models
            logging.info(f'Importing previous trained model from path : {self.model_resolver.get_latest_model_path()}')
            prev_model = load_obj(file_path=self.model_resolver.get_latest_model_path())

            logging.info(f'Importing previous transformer from path : {self.model_resolver.get_latest_transformer_path()}')
            prev_transformer = load_obj(file_path=self.model_resolver.get_latest_transformer_path())

            input_features = list(prev_transformer.feature_names_in_)
            input_array = prev_transformer.transform(X_test[input_features])
            prev_model_pred = prev_model.predict(input_array)

            prev_model_score = f1_score(prev_model_pred, y_test)
            logging.info(f'f1_score of previous trained model : {prev_model_score}')


            # check if current model accuracy is greater than previous model accuracy
            if curr_model_score <= prev_model_score:
                raise Exception(f"current model f1_score {curr_model_score} is less than previous model f1_score {prev_model_score}")
                
            # if yes then accept the current trained model else raise exception
            model_evaluation_artifact = artifact_entity.Model_evaluation_artifact(model_accepted=True, improved_accuracy=curr_model_score - prev_model_score)
            logging.info(f'================MODEL EVALUATION ARTIFACT================ : {model_evaluation_artifact}')
            return model_evaluation_artifact
        except Exception as e:
            raise PhishingException(e, sys)