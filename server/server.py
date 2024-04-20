from pdf_reader.pdf_reader import PdfReader
from rag.rag_retrieval import RagPipeline
# from models.qna_generation_model import QNAGenerationModel
from folder_manager.temp_folder_manager import TempFolderManager
from dotenv import load_dotenv
from flask import Flask, request, send_file
from flask_cors import CORS

import os
import pandas as pd 
import json

from models.qna_generation_model_new import QNAGenerationModel
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
temp_folder_manager = TempFolderManager()


@app.route('/questions', methods=['POST', 'GET'])
def get_questions():

    open_ended_count, mcq_count = int(request.args.get("open-ended-count")), int(request.args.get("mcq-count"))
    input_type = request.args.get("input-type")
    module_code = request.args.get("module-code")

    upload_folder = temp_folder_manager.create_temp_folder()

    questions = []

    try:
        # Loop through each pdf file uploaded by the user 
        for file_key in request.files:

            # Save uploaded file to upload_folder
            pdf_file = request.files[file_key]
            pdf_name = pdf_file.filename
            save_path = os.path.join(upload_folder, pdf_name)
            pdf_file.save(save_path)
            
            # Extract texts from pdf file
            texts = pdf_reader.get_text("tmp/" + pdf_name, input_type)

            # Combine texts with relevant content from RAG
            if input_type == "sample-question":

                oe_content = []
                oe_results = rag_pipeline.search_database_random(open_ended_count, module_code)
                for oe_result in oe_results:
                    oe_content.append(oe_result["content"])
                # oe_questions = qna_generation_model.generate_open_ended(context_list=oe_content, count=open_ended_count, question_style=texts[0])
                oe_questions = qna_generation_model.generate_questions(contents=oe_content, num_qns=open_ended_count, open_ended=True, formatting=texts[0])

                mcq_content = []
                mcq_results = rag_pipeline.search_database_random(mcq_count, module_code)
                for mcq_result in mcq_results:
                    mcq_content.append(mcq_result["content"])
                # mcq_questions = qna_generation_model.generate_mcq(context_list=mcq_content, count=mcq_count, question_style=texts[0])
                mcq_questions = qna_generation_model.generate_questions(contents=mcq_content, num_qns=mcq_count, mcq=True, formatting=texts[0])

            else:
                contents = []
                for text in texts:
                    first, second = rag_pipeline.search_database(text, module_code)
                    # contents.append(text + first["content"])
                    contents.append(first["content"])

                # oe_questions = qna_generation_model.generate_open_ended(context_list=contents, count=open_ended_count)
                # mcq_questions = qna_generation_model.generate_mcq(context_list=contents, count=mcq_count)
                oe_questions = qna_generation_model.generate_questions(contents=contents, num_qns=open_ended_count, open_ended=True, complimentary_info=texts)
                mcq_questions = qna_generation_model.generate_questions(contents=contents, num_qns=mcq_count, mcq=True, complimentary_info=texts)

            questions = questions + oe_questions + mcq_questions

        temp_folder_manager.remove_temp_folder()

        return create_excel_file(questions)
        
    except Exception as e:
        return "PDF cannot be read"


def create_excel_file(questions):
    """
    Creates an excel file containing 7 columns (Question, Choice A, Choice B, Choice C, Choice D, Answer, Explanation).

    Args:
        questions (list): List of JSON formatted strings containing question, answer and explanation data.

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

    # Iterate over each JSON string to extract the problems, choices, answers and explanations
    for data in questions:
        data = data.replace("\n", "").replace('\"', '"')
        data = json.loads(data)
        for qae in data["Output"]:
            problems.append(qae["Question"])
            answers.append(qae["Answer"])
            explanations.append(qae["Explanation"])
            choices = qae.get("Choices", None)
            choice_a.append(choices["a"] if choices else None)
            choice_b.append(choices["b"] if choices else None)
            choice_c.append(choices["c"] if choices else None)
            choice_d.append(choices["d"] if choices else None)
        
    
    # Creates a pandas DataFrame from the lists.
    df = pd.DataFrame({'Question': problems, 'Choice A': choice_a, 'Choice B': choice_b, 'Choice C': choice_c, 'Choice D': choice_d, 'Answer': answers, 'Explanation': explanations})

    # Save the DataFrame to an Excel file named "output.xlsx"
    df.to_excel("output.xlsx", index=False)

    # Return the Excel file as a response
    return send_file('output.xlsx', as_attachment=True)

if __name__ == "__main__":
    app.run(port=5001)