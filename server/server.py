from dotenv import load_dotenv
from flask import Flask, request, send_file
from flask_cors import CORS
from folder_manager.temp_folder_manager import TempFolderManager
from models.qna_generation_model import QNAGenerationModel
from pdf_reader.pdf_reader import PdfReader
from rag.rag_retrieval import RagPipeline

import json
import os
import pandas as pd
import random

app = Flask(__name__)
CORS(app)

# Load variables from .env file
load_dotenv()

# Access the loaded variables
db_user, db_pass = os.getenv("RAG_DATABASE_USERNAME"), os.getenv("RAG_DATABASE_PASSWORD")
h2o_api_key = os.getenv("H2O_API_KEY")

# Initalise classes for RAG, pdf reading, QA geneneration model, and folder manager
rag_pipeline = RagPipeline(db_user, db_pass)
pdf_reader = PdfReader()
qna_generation_model = QNAGenerationModel(h2o_api_key)
temp_folder_manager = TempFolderManager()


@app.route('/questions', methods=['POST', 'GET'])
def get_questions():
    """
    API endpoint to generate questions based on uploaded PDF files.

    Returns:
        flask.Response: A Flask response object containing the generated Excel file as an attachment.
    """
    
    # Retrieve parameters for the question generation
    open_ended_count, mcq_count = int(request.args.get("open-ended-count")), int(request.args.get("mcq-count"))
    module_code = request.args.get("module-code")
    input_type = request.args.get("input-type")
    is_sample_qns = input_type == "format"
    is_context = input_type == "context"

    # Create a temporary folder to store uploaded files
    upload_folder_path = temp_folder_manager.create_temp_folder()

    questions = []
    try:

        # Loop through each pdf file uploaded by the user 
        for file_key in request.files:

            # Save uploaded file to temporary folder
            pdf_file = request.files[file_key]
            pdf_name = pdf_file.filename
            save_path = os.path.join(upload_folder_path, pdf_name)
            pdf_file.save(save_path)
            
            # Extract texts from pdf file
            texts = pdf_reader.get_text("tmp/" + pdf_name, input_type)

            # Shuffle text chunks to reduce chances of question similarity
            random.shuffle(texts)

            # Retrieve most relevant content from vectorised database per text chunk
            contents = []
            for text in texts:
                first, second = rag_pipeline.search_database(text, module_code)
                contents.append(first["content"])

            open_ended_qns = qna_generation_model.generate_questions(contents=contents, user_input=texts, num_qns=open_ended_count, 
                                                                     open_ended=True, formatting=is_sample_qns, complimentary_info=is_context)

            # Reverse content and user input to further reduce similarity between MCQs and open ended questions
            contents.reverse()
            texts.reverse()

            mcq_questions = qna_generation_model.generate_questions(contents=contents, user_input=texts, num_qns=mcq_count, 
                                                                    mcq=True, formatting=is_sample_qns, complimentary_info=is_context)

            questions += open_ended_qns + mcq_questions

        temp_folder_manager.remove_temp_folder()
        return create_excel_file(questions, open_ended_count, mcq_count)
        
    except Exception as e:
        return "PDF cannot be read"


def create_excel_file(questions, open_ended_count, mcq_count):
    """
    Creates an excel file containing 7 columns (Question, Choice A, Choice B, Choice C, Choice D, Answer, Explanation).

    Args:
        questions (list): List of JSON formatted strings containing question, answer and explanation data.
        open_ended_count (int): Number of open ended questions that is expected to be in the excel file.
        mcq_count (int): Number of MCQs that is expected to be in the excel file.


    Returns:
        flask.Response: A Flask response object containing the generated Excel file as an attachment.
    """
    problems = []
    choice_a = []
    choice_b = []
    choice_c = []
    choice_d = []
    answers = []
    explanations = []

    output_open_ended_count = 0
    output_mcq_count = 0

    # Iterate over each JSON string to extract the problems, choices, answers and explanations
    for data in questions:
        data = data.replace("\n", "").replace('\"', '"')
        data = json.loads(data)
        for qae in data["Output"]:
            choices = qae.get("Choices", None)
            if choices and output_mcq_count < mcq_count:
                choice_a.append(choices["a"])
                choice_b.append(choices["b"])
                choice_c.append(choices["c"])
                choice_d.append(choices["d"])
                problems.append(qae["Question"])
                answers.append(qae["Answer"])
                explanations.append(qae["Explanation"])
                output_mcq_count += 1
            elif output_open_ended_count < open_ended_count:
                choice_a.append(None)
                choice_b.append(None)
                choice_c.append(None)
                choice_d.append(None)
                problems.append(qae["Question"])
                answers.append(qae["Answer"])
                explanations.append(qae["Explanation"])
                output_open_ended_count += 1
    
    # Creates a pandas DataFrame from the lists
    df = pd.DataFrame({'Question': problems, 'Choice A': choice_a, 'Choice B': choice_b, 'Choice C': choice_c, 'Choice D': choice_d, 'Answer': answers, 'Explanation': explanations})

    # Save the DataFrame to an Excel file named "output.xlsx"
    df.to_excel("output.xlsx", index=False)

    # Return the Excel file as a response
    return send_file('output.xlsx', as_attachment=True)

if __name__ == "__main__":
    app.run(port=5001)
    