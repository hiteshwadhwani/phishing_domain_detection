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
    model_path:str
    train_score:float
    test_score:float

@dataclass
class Model_evaluation_artifact:
    model_accepted:bool
    improved_accuracy:float

@dataclass
class Model_pusher_artifact:
    model_path:str
    transformer_path:str

