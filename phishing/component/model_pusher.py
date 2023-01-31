from phishing.entity import config_entity, artifact_entity
from phishing.predictor import ModelResolver
from phishing.exception import PhishingException
import os,sys
from phishing import utils
from phishing.logger import logging

class Model_pusher:
    def __init__(self, model_pusher_config:config_entity.Model_evaluation_config,
                data_transformation_artifact:artifact_entity.Data_transformation_artifact,
                model_builder_artifact:artifact_entity.Model_builder_artifact):
        
        logging.info(f'{2 * "<<"} MODEL PUSHER {2 * ">>"}')
        self.model_pusher_config = model_pusher_config
        self.data_transformation_artifact = data_transformation_artifact
        self.model_builder_artifact = model_builder_artifact
        self.model_resolver = ModelResolver(model_registory='saved_models',
                                            transformer_dir_name='transformer',
                                            model_dir_name='model')
    def intiate_model_pusher(self):
        try:
            model = utils.load_obj(file_path=self.model_builder_artifact.model_path)
            transformer = utils.load_obj(file_path=self.data_transformation_artifact.transform_obj_file_path)

            # saving model and transformer in artifact folder
            utils.save_object(file_path=self.model_pusher_config.model_pusher_model_path, object=model)
            utils.save_object(file_path=self.model_pusher_config.model_pusher_transformer_path, object=transformer)

            # get latest model registory model and transfoemer path
            model_path = self.model_resolver.get_latest_save_model_path()
            transformer_path = self.model_resolver.get_latest_save_transformer_path()
            
            # save model and transformer in model_registory
            utils.save_object(file_path=model_path, object=model)
            utils.save_object(file_path=transformer_path, object=transformer)

            model_pusher_artifact = artifact_entity.Model_pusher_artifact(model_path=model_path,
                                                                          transformer_path=transformer_path)

            return model_pusher_artifact
            
        except Exception as e:
            raise PhishingException(e, sys)