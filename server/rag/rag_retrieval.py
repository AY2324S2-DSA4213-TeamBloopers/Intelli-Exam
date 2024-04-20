from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from sentence_transformers import SentenceTransformer

import certifi

class RagPipeline:
    """Class for performing search operations on a MongoDB database using vector search."""

    def __init__(self, username, password):
        """
        Initialises the RagPipeline object.

        Parameters:
        - username (str): The username for accessing the MongoDB database.
        - password (str): The password for accessing the MongoDB database.
        """
        self.uri_generator = lambda username, password: f"mongodb+srv://{username}:{password}@rag-database.aqvwmxz.mongodb.net/?retryWrites=true&w=majority"
        self.client = MongoClient(self.uri_generator(username=username, password=password), server_api=ServerApi("1"), tlsCAFile=certifi.where())
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

    def embed_query(self, query):
        return self.embedding_model.encode(query).tolist()

    def get_pipeline(self, query_embedding):
        """
        Generates the aggregation pipeline for performing vector search.

        Parameters:
        - query_embedding (list of float): The embedding vector of the query.

        Returns:
        - list: The aggregation pipeline.
        """
        self.pipeline[0]["$vectorSearch"]["queryVector"] = query_embedding
        return self.pipeline

    def search_database(self, query, course_code):
        """
        Searches the MongoDB database for relevant documents based on the query.

        Parameters:
        - query (str): The search query.
        - course_code (str): The code of the course corresponding to the database collection.

        Returns:
        - list of dict: List of documents matching the search query.
        """
        collection = self.client[course_code]["content"]
        query_embedding = self.embed_query(query)
        pipeline = self.get_pipeline(query_embedding)
        results = list(collection.aggregate(pipeline))
        return results
