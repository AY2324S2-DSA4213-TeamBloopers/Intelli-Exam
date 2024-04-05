"""
Script for initialising a MongoDB database with course content.
Please note: This code should not be run again and is kept for tracking purposes.
"""

from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from sentence_transformers import SentenceTransformer

import certifi
import os
import PyPDF2

embedding_model = SentenceTransformer("thenlper/gte-large")

def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)     
        page = reader.pages[0]
        text = page.extract_text()
        while text[:7] != "Summary":
            text = text[1:]
        return text[7:]

def initialise_database():
    pdf_values = [str(i) if len(str(i)) == 2 else "0" + str(i) for i in range(1, 11)]
    all_data = []
    for pdf_value in pdf_values:
        text = read_pdf(f'/database_data/L{pdf_value}_outline.pdf').replace("\no", "\n\to").strip()

        for i in text.split("\n \n"):
            title, content = i.split("\n", 1)
            all_data.append({"title": title.strip().replace(" -", "-"), "content": content, "embedding": embedding_model.encode(content).tolist()})

    load_dotenv()

    URI = os.getenv("RAG_DATABASE_URI")
    client = MongoClient(URI, server_api=ServerApi("1"), tlsCAFile=certifi.where())
    collection = client["computer_vision"]["content"]
    collection.insert_many(all_data)

if __name__ == "__main__":
    initialise_database()
