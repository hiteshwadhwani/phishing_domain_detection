import pymongo
from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()
@dataclass
class EnvironmentVariables:
    MONGO_DB_URL = os.getenv("MONGO_DB_URL")

my_env = EnvironmentVariables()

TARGET_FEATURE = 'phishing'

myclient = pymongo.MongoClient(my_env.MONGO_DB_URL)
print(myclient)


