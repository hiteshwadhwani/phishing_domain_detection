# batch pipeline imports dataset from 
from phishing.exception import PhishingException
import os,sys
import pandas as pd
from phishing.predictor import ModelResolver
from phishing.utils import load_obj
from phishing.logger import logging


PREDICTION_DIR_NAME = 'Prediction'

def batch_prediction(input_file_path:str):
    try:
        # Import data as dataframe from input file path
        logging.info(f'Import dataset from path {input_file_path}')
        df = pd.read_csv(filepath_or_buffer=input_file_path)

        # Import latest model ans transformer from saved_models dir
        model_resolver = ModelResolver()
        latest_model_path = model_resolver.get_latest_model_path()
        latest_transformer_path = model_resolver.get_latest_transformer_path()

        transformer  = load_obj(file_path=latest_transformer_path)
        model = load_obj(file_path=latest_model_path)

        # Transform dataset
        input_features = transformer.feature_names_in_
        input_arr = transformer.transform(df[input_features])
    
        # predit on data
        logging.info('Predicting data')
        prediction = model.predict(input_arr)
        prediction = transformer.inverse_transform(transformer)

        # save prediction in dataframe
        df["prediction"] = prediction

        # save df as csv in prediction folder
        file_name = os.path.basename(input_file_path.replace(".csv", f"{datetime.now().strftime('%m%d%Y__%H%M%S')}.csv"))
        file_path = os.path.join(PREDICTION_DIR_NAME, file_name)

        logging.info(f'saving prediction file to path {file_path}')
        df.to_csv(path_or_buf=file_path, header=True, index=False)
        return file_path
    except Exception as e:
        raise PhishingException(e, sys)