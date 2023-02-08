import pandas as pd
import numpy as np
from phishing.entity import config_entity, artifact_entity
import os,sys
from phishing.logger import logging
from scipy.stats import ks_2samp
from phishing import utils
from phishing.exception import PhishingException

class Data_validation:
    def __init__(self, data_validation_config:config_entity.Data_validation_config, data_ingestion_artifact:artifact_entity.Data_ingestion_artifact):
        logging.info(f'{10 * "<<"} DATA VALIDATION {10 * ">>"}')
        self.data_validation_config = data_validation_config
        self.data_ingestion_artifact = data_ingestion_artifact
        self.validation_report = dict()

    def drop_columns_with_null_values(self, current_df:pd.DataFrame, validation_report_key:str):
        try:
            missing_percentage = current_df.isna().sum().div(current_df.shape[0]).mul(100)
            threshold = self.data_validation_config.missing_values_threshold
            missing_percentage_columns = missing_percentage[missing_percentage.values>threshold]
            current_df.drop(missing_percentage_columns, axis=1, inplace=True)
            self.validation_report[validation_report_key] = len(missing_percentage_columns)
            
            if len(current_df.columns) == 0:
                return None
            return current_df
        except Exception as e:
            raise PhishingException(e, sys)
    def check_data_drift(self, base_df:pd.DataFrame, current_df:pd.DataFrame, validation_report_key:str):
        try:
            data_drift = dict()
            base_col = base_df.columns
            current_col = current_df.columns

            for col in base_col:
                base_data = base_df[col]
                current_data = current_df[col]
                p_val = float(ks_2samp(base_data, current_data).pvalue)
                
                # null hypothesis -> base_data and current_data belong to same distribution
                # alternate hypothesis -> base_data and current_data belong to different distribution
                if p_val < 0.05:
                    # accept alternate hypothesis
                    self.validation_report[col] = {
                        'p_value':p_val,
                        'same_distribution':False
                    }
                else:
                    # fail to reject null hypothesis
                    self.validation_report[col] = {
                        'p_value':p_val,
                        'same_distribution':True
                    }

            self.validation_report[validation_report_key] = data_drift
        except Exception as e:
            raise PhishingException(e, sys)
    def check_missing_columns(self, base_df:pd.DataFrame, current_df:pd.DataFrame, validation_report_key:str):
        try:
            base_df_columns = base_df.columns
            current_df_columns = current_df.columns

            missing_columns = []

            for base_col in base_df_columns:
                if base_col not in current_df_columns:
                    missing_columns.append(base_col)

            if len(missing_columns) > 0:
                self.validation_report[validation_report_key] = missing_columns
                return False
            return True
        except Exception as e:
            raise PhishingException(e, sys)
    def intiate_data_validaiton(self):
        try:
            # import current df
            logging.info("importing train_df and test_df")
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            # Import base_df
            logging.info("importing base_df")
            url = 'https://drive.google.com/file/d/1zwUKSiaEM43A875jAUmqCKQ3ooxo8XIS/view?usp=share_link'
            url='https://drive.google.com/uc?id=' + url.split('/')[-2]
            base_df = pd.read_csv(url)

            # drop columns with missing values greater than 30 %
            logging.info("Dropping columns with null values greater than 70% (default)")
            train_df = self.drop_columns_with_null_values(train_df, 'missing_values_within_train_dataset')
            test_df = self.drop_columns_with_null_values(test_df, 'missing_values_within_test_dataset')

            # Check for the number of features between base_df and current_df
            logging.info("Checking missing columns")
            train_df_column_status = self.check_missing_columns(base_df, train_df, 'missing_column_within_train_dataset')
            test_df_column_status = self.check_missing_columns(base_df, test_df, 'missing_column_within_test_dataset')

            logging.info("checking data drift")
            # Check data drift
            if train_df_column_status:
                self.check_data_drift(base_df, train_df, 'validation_report_train_dataset')

            if test_df_column_status:
                self.check_data_drift(base_df, test_df, 'validation_report_test_dataset')
            
            # convert validation dictionary into YAML file
            logging.info('Creating YAML file and saving validation report')
            utils.create_YAML_file(self.data_validation_config.data_validation_report, self.validation_report)

            # data_validation_artifact
            logging.info('creating data_validation artifact')
            data_validation_artifact = artifact_entity.Data_validation_artifact(validation_report_file=self.data_validation_config.data_validation_report)

            logging.info(f"=================DATA VALIDATION ARTIFACT=============== : {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise PhishingException(e, sys)