<p><h1 align="center"> 

![Intelli-Exam](https://gcdnb.pbrd.co/images/K5lQygPw4F84.png?o=1) 
</h1></p>


<h2 align="center">    
    
Hassle-free question generation for all educators
    
</h2>

<div>
<h3 align="center">    
Project Description
</h3>
Intelli-Exam knows that educators are busy individuals, having to juggle many responsibilities. Furthermore, they are unable to resuse old exam questions as students normally seek them out for practice. The app provides a solution implementing RAG and LLMs to generate questions. The model generates MCQs and Open-Ended questions, and allows equcators to provide complimentary information to switch up the questions whilst still focusing on the syllabus.
</div>

<p><h1 align="center"> Table of Contents </h1></p>

 1) [Solution Architecture](#solution-architecture)
 2) [Tech Stack](#tech-stack)
 3) [Getting Started](#start-up)
 4) [Dependencies](#dependencies)
 5) [User Guide](#user-guide)
 6) [Credits](#credits)

<a name="solution-architecture"></a>
<p><h1 align="center"> Solution Architecture </h1></p>  

<h2 align="center">
    <a href="https://pasteboard.co/O3hf9asyhEG0.jpg" target="blank_">
        <img alt="Solution Architecture" src="https://gcdnb.pbrd.co/images/O3hf9asyhEG0.jpg?o=1" width="800" height="200" />
    </a>
</h2>

<a name="tech-stack"></a>
<p><h1 align="center"> Tech Stack </h1></p>  

1. **React**
    - Frontend library for building interactive UI components
2. **Python**
    - Backend language utilized for server-side logic, data processing, API development, and building the pipeline.
3. **Flask**
    - Lightweight Python web framework used for building RESTful APIs and serving backend functionalities
4. **MongoDB**
    - NoSQL database used for RAG retrieval.
5. **H2OGPTE**
    - H2OGPTE, developed by H2O.ai, provides the large language model used in this project via API calls.

<a name="start-up"></a>
<p><h1 align="center"> Getting Started </h1></p>  
Create a python environment by running the following commands (this is assuming Python is installed properly).

For MacOS / Linux:

```sh
python3 -m venv venv
source venv/bin/activate
pip install -r server/requirements.txt
```

For Windows:

```sh
python3 -m venv venv
venv\Scripts\activate
pip install -r server\requirements.txt
```

Next install required dependencies in 'package.json' file. Then start the server.

```sh
npm install
npm start
```
In another terminal, run server.py
```sh
python server\server.py
```

.env file needs to be in the server folder, containing:

**RAG_DATABASE_USERNAME**

**RAG_DATABASE_PASSWORD**

**H2O_API_KEY**

<a name="dependencies"></a>
<p><h1 align="center"> Dependencies </h1></p>  

1) Python 3.9.6
2) NPM 10.5.0

<a name="user-guide"></a>
<p><h1 align="center"> User Guide </h1></p>  

Intelli-Exam should already have all the required information from the syllabus uploaded. If you can find the NUS module from the "NUS Module" drop down selector, you can generate questions from the module.

Select "Type Of Upload" and select the type of upload you are going to make. It can either be sample questions or context. For sample questions, the questions generated will attempt to follow the style of questions in the file. 
For context, the questions generated will attempt to form questions using the complimentary information provided whilst still focusing on the syllabus.

Upload the file by presing "Browse files". Take note the app will only accept doc or pdf files.

You can select the number of MCQ and Open ended questions you want to generate, from 0 to 20.

Finally, press submit and the questions will be sent over in excel format.

<a name="credits"></a>
<p><h1 align="center"> Credits </h1></p>  
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
