import os,sys
from phishing.entity.config_entity import MODEL_FILE_NAME, TRANSFORM_FILE_NAME
from phishing.exception import PhishingException

class ModelResolver:
    def __init__(self, model_registory='saved_models', transformer_dir_name='transformer', model_dir_name='model'):
        self.model_registory = model_registory
        os.makedirs(model_registory, exist_ok=True)
        self.transformer_dir_name = transformer_dir_name
        self.model_dir_name = model_dir_name

    def get_latest_dir_path(self):
        try:
            dir_names = os.listdir(self.model_registory)

            if len(dir_names) == 0:
                return None

            dir_names = list(map(int, dir_names))
            latest_dir_name = max(dir_names)
            return os.path.join(self.model_registory, latest_dir_name)
        except Exception as e:
            raise PhishingException(e, sys)    
        

    def get_latest_model_path(self):
        try:
            latest_dir = self.get_latest_dir_path()

            if latest_dir is None:
                raise Exception("No model Found")

            model_path = os.path.join(latest_dir, self.transformer_dir_name, MODEL_FILE_NAME)
            return model_path
        except Exception as e:
            raise PhishingException(e, sys)

    def get_latest_transformer_path(self):
        try:
            latest_dir = self.get_latest_dir_path()

            if latest_dir is None:
                raise Exception('No transformer found')

            transformer_path = os.path.join(latest_dir, self.transformer_dir_name, TRANSFORM_FILE_NAME)
        except Exception as e:
            raise PhishingException(e, sys)


    def get_latest_save_dir_path(self):
        try:
            latest_dir = self.get_latest_dir_path()

            if latest_dir is None:
                return os.path.join(self.model_registory, f"{0}")
            
            latest_dir_num = int(os.path.basename(latest_dir))
            return os.path.join(self.model_registory, f"{latest_dir_num + 1}")
        except Exception as e:
            raise PhishingException(e, sys)


    def get_latest_save_model_path(self):
        try:
            return os.path.join(self.get_latest_save_dir_path(), self.model_dir_name, MODEL_FILE_NAME)
        except Exception as e:
            raise PhishingException(e, sys)



    def get_latest_save_transformer_path(self):
        try:
            return os.path.join(self.get_latest_save_dir_path(), self.transformer_dir_name, TRANSFORM_FILE_NAME)
        except Exception as e:
            raise PhishingException(e, sys)


        
        

        
        


