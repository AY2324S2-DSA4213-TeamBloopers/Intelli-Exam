from pdf_reader.pdf_reader import PdfReader
from rag.rag_retrieval import RagPipeline
from dotenv import load_dotenv
from flask import Flask, request
from flask_cors import CORS

import os
import shutil

app = Flask(__name__)
CORS(app)

# Load variables from .env file
load_dotenv()

# Access the loaded variables
db_user, db_pass = os.getenv("RAG_DATABASE_USERNAME"), os.getenv("RAG_DATABASE_PASSWORD")

rag_pipeline = RagPipeline(db_user, db_pass)
pdf_reader = PdfReader()


@app.route('/questions', methods=['POST', 'GET'])
def get_questions():
    upload_folder = create_temp_folder()

    try:
        for file_key in request.files:
            # Get uploaded file 
            pdf_file = request.files[file_key]
            # Get file name
            pdf_name = pdf_file.filename
            # Save uploaded file to upload_folder
            save_path = os.path.join(app.config.get('upload_folder'), pdf_name)
            pdf_file.save(save_path)
            
            texts = pdf_reader.get_text("tmp/" + pdf_name)
            for text in texts:
                first, second = rag_pipeline.search_database(text)

        remove_temp_folder(upload_folder)

        return first
        # return "Questions successfully generated", excel file
        
    except Exception as e:
        return "PDF can't be read"
    
def create_temp_folder():
    try:
        # Gives absolute path of directory
        path = os.path.dirname(os.path.abspath(__file__)) 
        # Save file outside main directory in folder named "tmp"
        upload_folder=os.path.join(path.replace("/file_folder",""),"tmp")
        # Create directory recursively 
        os.makedirs(upload_folder, exist_ok=True)
        # Add configuration path in app for "upload_folder"
        app.config['upload_folder'] = upload_folder
        return upload_folder
    except Exception as e:
        return "Folder could not be created"
        
def remove_temp_folder(upload_folder):
    shutil.rmtree(upload_folder)
    

if __name__ == "__main__":
    app.run(port=5001)