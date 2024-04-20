"""
Script for initialising a MongoDB database with DSA4213 course content.
Please note: This code should not be run again and is kept for tracking purposes.
"""

from dotenv import load_dotenv
from pdfminer.high_level import extract_text
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from sentence_transformers import SentenceTransformer

import certifi
import os

embedding_model = SentenceTransformer("thenlper/gte-large")

def read_pdf():
    texts = []

    # For every lecture notes, extract content in chunks, remove common gibberish of symbols. Not perfectly extracted, but sufficient for the project.
    for i in range(2, 8):
        k = extract_text(f"rag/database_data/DSA4213-Lecture{i}.pdf").strip().replace("!\"#$%&’()*+\",-+($.-/\"0.(12’3(+&\"$4\"5(.)-%$’26\"7//\"8()*+3\"8232’1296\"", "").split("\n\n")
        j = 0
        text = ""
        for i in k:
            text += i
            if i == "":
                j += 1
            if j == 10:
                texts.append(text)
                text = ""
                j = 0
        texts.append(text)
    return texts

def initialise_database():
    texts = read_pdf()

    load_dotenv()
    URI = os.getenv("RAG_DATABASE_URI")
    client = MongoClient(URI, server_api=ServerApi("1"), tlsCAFile=certifi.where())
    collection = client["DSA4213"]["content"]

    embeddings = list(map(lambda x: embedding_model.encode(x).tolist(), texts))
    docs = [{"content": content, "embedding": embedding} for content, embedding in zip(texts, embeddings)]
    collection.insert_many(docs)

if __name__ == "__main__":
    initialise_database()
