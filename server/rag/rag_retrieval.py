from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from sentence_transformers import SentenceTransformer

import certifi

class RagPipeline:
    def __init__(self, username, password):
        self.uri_generator = lambda username, password: f"mongodb+srv://{username}:{password}@rag-database.aqvwmxz.mongodb.net/?retryWrites=true&w=majority"
        self.client = MongoClient(self.uri_generator(username=username, password=password), server_api=ServerApi("1"), tlsCAFile=certifi.where())
        self.collection = self.client["computer_vision"]["content"]
        self.embedding_model = SentenceTransformer("thenlper/gte-large")
        self.pipeline = [{
            "$vectorSearch": {
                "index": "rag_vector_search",
                "queryVector": None,
                "path": "embedding",
                "numCandidates": 150,
                "limit": 2,
            }},{
            "$project": {
                "_id": 0,
                "title": 1,
                "content": 1,
                "score": {"$meta": "vectorSearchScore"},
            }}]

    def get_pipeline(self, query_embedding):
        self.pipeline[0]["$vectorSearch"]["queryVector"] = query_embedding
        return self.pipeline
    
    def embed_query(self, query):
        return self.embedding_model.encode(query).tolist()

    def search_database(self, query):
        query_embedding = self.embed_query(query)
        pipeline = self.get_pipeline(query_embedding)
        results = list(self.collection.aggregate(pipeline))
        return results
    