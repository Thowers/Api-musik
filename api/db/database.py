from pymongo import MongoClient, ASCENDING

class Database:
    def __init__(self):
        self.client = MongoClient("mongodb+srv://towers1904:nikolash190499@clusterthowers.ixmyw.mongodb.net/?retryWrites=true&w=majority&appName=ClusterThowers", tlsallowinvalidcertificates=True)
        self.db = self.client["musik"]
        self._ensure_indexes()

    def _ensure_indexes(self):
        col = self.db["noticias"]
        col.create_index([("link", ASCENDING)], unique=True)

    def get_collection(self, collection):
        return self.db[collection]

database = Database()