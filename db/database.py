from pymongo import MongoClient, ASCENDING
import os  
from dotenv import load_dotenv 

load_dotenv()
class Database:
    def __init__(self):
        self.client = MongoClient(os.getenv("MONGO"), tlsallowinvalidcertificates=True)
        self.db = self.client[os.getenv("DB")]
        self._ensure_indexes()

    def _ensure_indexes(self):
        col = self.db[os.getenv("COLLECTION")]
        col.create_index([("link", ASCENDING)], unique=True)

    def get_collection(self, collection):
        return self.db[collection]

database = Database()