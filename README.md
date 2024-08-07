# DSA4213 Team Bloopers: Intelli-Exam
Hassle-free questions generation for NUS educators

## Project Description

Team Bloopers recognises the busy schedules of university educators. With Intelli-exam, we attempt to employ our proprietary RAG Pipeline, integrated with h2oGPTe's API to run their LLM model for generation of exam questions. 

Question types include MCQs or open-ended, with educators having the flexibility to execute two query types:

- **Sample Questions**: Useful in generating consistent exam question format throughout every semesters, without repeating questions

- **Additional Context**: Useful in generating questions that rely on context, especially for courses that are continuously advancing in landscape


## Vectorised Database

Our vectorised database stores syllabus content from NUS courses. With our RAG pipeline, we minimise the chances of the LLM hallucinating with inaccurate information, while at the same time ensuring questions generated stay within the syllabus of the courses.

## File Structure

```bash
- Intelli-Exam/
  ├── client/
  │   ├── src
  │   │   └── ...
  │   ├── package.json
  │   └── package-lock.json
  ├── server/
  │   ├── folder_manager
  │   │   └── temp_folder_manager.py
  │   ├── models
  │   │   └── qna_generation_model.py
  │   ├── pdf_reader
  │   │   └── pdf_reader.py
  │   ├── rag
  │   │   ├── database_setup.py
  │   │   └── rag_retrieval.py
  │   ├── requirements.txt
  │   └── server.py
  ├── .gitignore
  └── README.md
```


## Tech Stack

- **React**: Frontend library for building interactive UI components

- **Flask**: Provides a RESTful API backend, allowing communication between the frontend and backend.

- **MongoDB Atlas**: A cloud-based NoSQL database, for vector search capabilities.

- **H2OGPTE**: H2OGPTE, developed by H2O.ai, provides the large language model used in this project via API calls.


## Getting Started

1. Ensure you have Python and Node.js installed on your system:

   - Python: You can download Python from the [official website](https://www.python.org/downloads/). Make sure to add Python to your system's PATH during installation.
   - Node.js: You can download Node.js from the [official website](https://nodejs.org/). Follow the installation instructions for your operating system.

2. Clone the repository:

    ```bash
    git clone https://github.com/AY2324S2-DSA4213-TeamBloopers/Intelli-Exam.git
    cd Intelli-Exam
    ```

3. Install React dependencies:

    ```bash
    cd client
    npm install
    ```

4. Install Python dependencies in a virtual environment:

    For MacOS/Linux:
    ```bash
    cd ../server
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

    For Windows
    ```bash
    cd ../server
    python3 -m venv venv
    venv/Scripts/activate
    pip install -r requirements.txt
    ```

5. In the same terminal, run the server:
    ```bash
    python3 server.py
    ```

6. Without closing the current terminal, create a new terminal and start the react instance:
    ```bash 
    cd client
    npm start
    ```
    
The website is then run at: http://localhost:3000/


## User Guide

Intelli-Exam should already have all the required content within the syllabus uploaded in its database. If you can find the NUS module from the "NUS Module" drop down selector, you can generate questions from the module.

Under "Type Of Upload", select the type of documents that are going to be used. It can either be sample questions or context. For sample questions, the questions generated will attempt to follow the style of questions in the file. 
For context, the questions generated will attempt to form questions using the complimentary information provided whilst still focusing on the syllabus.


Upload the files by presing "Browse files". Take note that the Intelli-Exam currently accepts pdf files only.

You can select the number of MCQ and open-ended questions you want to generate, between 0 to 20.

Finally, press submit and wait for the excel file to download on your browser!


## Current Limitations

- Due to copyright issues, we currently only support content and question generation for DSA4213. Addition course codes in the dropdown are meant to be placeholders, selecting them for generation will execute for DSA4213.

- Due to our batching strategy when generating question and answers pair, do expect to wait for a few minutes generating beyond tens of questions.


## Contributors 
<div>
 <table>
  <tr>
    <th>No.</th>
    <th>Contributers</th>
    <th>GitHub Link</th>
  </tr>
  <tr>
    <td>1</td>
    <td>Lee Zhan Peng</td>
    <td><a href="https://github.com/leezhanpeng" target="blank_">
    GitHub</a>
    </td>
  </tr>
  <tr>
    <td>2</td>
    <td>Jennifer Chue</td>
    <td><a href="https://github.com/jenniferchue16" target="blank_">
    GitHub</a>
    </td>
  </tr>
   <tr>
    <td>3</td>
    <td>Celeste Neo</td>
    <td><a href="https://github.com/celneo7" target="blank_">
    GitHub</a>
    </td>
  </tr>
  <tr>
    <td>4</td>
    <td>Lincoln Teo</td>
    <td><a href="https://github.com/BreatheManually" target="blank_">
    GitHub</a>
    </td>
  </tr>
</table> 
