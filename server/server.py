from pdf_reader.pdf_reader import PdfReader
from rag.rag_retrieval import RagPipeline
from models.qna_generation_model import QNAGenerationModel
from dotenv import load_dotenv
from flask import Flask, request, send_file
from flask_cors import CORS

import os
import shutil
import pandas as pd 
import json

app = Flask(__name__)
CORS(app)

# Load variables from .env file
load_dotenv()

# Access the loaded variables
db_user, db_pass = os.getenv("RAG_DATABASE_USERNAME"), os.getenv("RAG_DATABASE_PASSWORD")
h2o_api_key = os.getenv("H2O_API_KEY")

rag_pipeline = RagPipeline(db_user, db_pass)
pdf_reader = PdfReader()
qna_generation_model = QNAGenerationModel(h2o_api_key)


@app.route('/questions', methods=['POST', 'GET'])
def get_questions():
    upload_folder = create_temp_folder()

    questions = []

    try:
        # Loop through each pdf file uploaded by the user 
        for file_key in request.files:
            contents = []

            # Save uploaded file to upload_folder
            pdf_file = request.files[file_key]
            pdf_name = pdf_file.filename
            save_path = os.path.join(app.config.get('upload_folder'), pdf_name)
            pdf_file.save(save_path)
            
            # Extract texts from pdf file
            texts = pdf_reader.get_text("tmp/" + pdf_name)

            # Combine texts with relevant content from RAG
            for text in texts:
                first, second = rag_pipeline.search_database(text)
                contents.append(text + first["content"])

            question = qna_generation_model.generate_all(context_list=contents)
            questions.append(question)


        remove_temp_folder(upload_folder)

        return create_excel_file(questions)
        
    except Exception as e:
        raise e
        return "PDF cannot be read"
    
def create_temp_folder():
    """
    Creates a temporary folder as a placeholder for all uploaded pdf files from the user.

    Returns:
        upload_folder (str): String of the absolute path to the directory where the uploaded pdf files will be stored. 
    """
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
    """
    Deletes the temporary folder containing all uploaded pdf files from the user. 
    """
    shutil.rmtree(upload_folder)


def create_excel_file(questions):
    """
    Creates an excel file containing 3 columns (Question, Answer, Explanation).

    Args:
        questions (list): List of JSON formatted strings containing question, answer and explanation data.

    Returns:
        flask.Response: A Flask response object containing the generated Excel file as an attachment.
    """
    problems = []
    answers = []
    explanations = []

    # Iterate over each JSON string to extract the problems, answers and explanations
    for data in questions:
        data = data.replace("\n", "").replace('\"', '"')
        data = json.loads(data)
        for key, value in data.items():
            problems.append(value['Question'])
            answers.append(value['Answer'])
            explanations.append(value['Explanation'])
    
    # Creates a pandas DataFrame from the lists.
    df = pd.DataFrame({'Question': problems, 'Answer': answers, 'Explanation': explanations})

    # Save the DataFrame to an Excel file named "output.xlsx"
    df.to_excel("output.xlsx", index=False)

    # Return the Excel file as a response
    return send_file('output.xlsx', as_attachment=True)
    

if __name__ == "__main__":
    app.run(port=5001)