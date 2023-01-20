from dataclasses import dataclass

@dataclass
class Data_ingestion_artifact:
    feature_store_path:str
    train_file_path:str
    test_file_path:str

@dataclass
class Data_transformation_artifact:
    transform_obj_file_path:str
    train_file_path:str
    test_file_path:str

@dataclass
class Data_validation_artifact:
    validation_report_file:str

@dataclass
class Model_builder_artifact:
    pass

@dataclass
class Model_evaluation_artifact:
    pass

@dataclass
class Model_pusher_artifact:
    pass

