import pandas as pd
import numpy as np
from phishing.exception import PhishingException
from phishing.logger import logging
from phishing.config import TARGET_FEATURE
from sklearn.preprocessing import RobustScaler
from sklearn.pipeline import Pipeline
from phishing import utils
import os,sys
from phishing.entity import config_entity, artifact_entity 
from imblearn.combine import SMOTETomek




class Data_transformation:
    def __init__(self, data_transformation_config, data_ingestion_artifact):
        self.data_transformation_config = data_transformation_config
        self.data_ingestion_artifact = data_ingestion_artifact

    @classmethod
    def get_transformation_object(cls)->Pipeline:
        try:
            pipe = Pipeline([('rc_scaler', RobustScaler())])
            return pipe
        except Exception as e:
            PhishingException(e, sys)

    def intiate_data_transformation(self):
        try:
            logging.info("Importing train and test data")
            train_df = pd.read_csv(filepath_or_buffer=self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(filepath_or_buffer=self.data_ingestion_artifact.test_file_path)

            input_train_df = train_df.drop(TARGET_FEATURE, axis=1)
            output_train_df = train_df[TARGET_FEATURE]

            input_test_df = test_df.drop(TARGET_FEATURE, axis=1)
            output_test_df = test_df[TARGET_FEATURE]

            transformation_obj = Data_transformation.get_transformation_object()
            transformation_obj.fit(input_train_df)
            

            transformed_train_array =  transformation_obj.transform(input_train_df)
            transformed_test_array = transformation_obj.transform(input_test_df)

            # now oversample data using SMOTE
            smt = SMOTETomek(random_state=42)
            input_feature_train_arr, output_feature_train_arr = smt.fit_resample(transformed_train_array, output_train_df)
            input_feature_test_arr, output_feature_test_arr = smt.fit_resample(transformed_test_array, output_test_df)

            # concat input and output feature
            train_arr = np.c_[input_feature_train_arr, output_feature_train_arr]
            test_arr = np.c_[input_feature_test_arr, output_feature_test_arr]

            # save train and test data to artifact folder
            utils.save_numpy_array(file_path=self.data_transformation_config.train_file_path, array=train_arr)
            utils.save_numpy_array(file_path=self.data_transformation_config.test_file_path, array=test_arr)

            # save transformation obj to artifact folder
            print(self.data_transformation_config.data_transformation_obj_path)
            utils.save_object(file_path=self.data_transformation_config.data_transformation_obj_path, object=transformation_obj)

            data_transfrmation_artifact = artifact_entity.Data_transformation_artifact(transform_obj_file_path=self.data_transformation_config.data_transformation_obj_path,
            train_file_path=self.data_transformation_config.train_file_path,
            test_file_path=self.data_transformation_config.test_file_path)

            return data_transfrmation_artifact
        except Exception as e:
            raise PhishingException(e, sys)