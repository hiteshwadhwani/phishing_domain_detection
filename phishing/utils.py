import pandas as pd
from phishing.config import myclient

def get_collection_as_dataframe(database, collection)->pd.DataFrame:
    pass

print(list(myclient['phishing']['dataset'].find())[0])
