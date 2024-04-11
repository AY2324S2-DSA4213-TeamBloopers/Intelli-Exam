import React from "react"
import InputFile from "./InputFile"
import Dropdown from "./Dropdown"

import axios from "axios"


export default function Input(){

    const [opt, setOpt] = React.useState("")

    function handleOptChange(event){
        setOpt(event.target.value)
    }

    const [files, setFile] = React.useState([])

    function handleFile(event){
        const uploadedFiles = event.target.files;
        setFile([...files, ...uploadedFiles])
    }

    function handleDelete(index){
        setFile(files.toSpliced(index, 1))
    }


    const sendPDFToBackend = async () => {
        try {
            if (!files){
                console.log("no files")
            }
    
            const fd = new FormData()
            files.forEach((file, index) => {
                fd.append(`file${index+1}`, file)
            })
    
            const response = await axios.post('http://localhost:5001/questions', fd, {
                headers: {
                'Content-Type': 'multipart/form-data',
                },
                responseType:'blob'
            });

            const blob = new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
            
            // Create a temporary URL to the Excel file 
            const url = window.URL.createObjectURL(blob); 
        
            // Create a link and trigger the download 
            const link = document.createElement('a'); 
            link.href = url; 
            link.setAttribute('download', 'output.xlsx'); 
            document.body.appendChild(link); 
            link.click(); 

        
            console.log('PDF uploaded successfully:', response.data);
            } catch (error) {
            console.error('Error uploading PDF:', error);
            }
      };
    
    function handleSubmit(event){

        event.preventDefault();

        sendPDFToBackend();
    }

    return(

        <form onSubmit={handleSubmit} className="input-body">
            <h1 className="file--title">Upload slides or documents of the content you teach to generate Exam Q&As!</h1>
            
            <div className="input-grid">
                <InputFile 
                    upload={handleFile}
                    delete= {handleDelete}
                    files = {files}/>
        
                <div class="buttons">                    
                    <Dropdown
                        value={opt}
                        onChange={handleOptChange}/>
                    
                    <button className="btn btn-primary" value="Submit" onChange={handleSubmit}>
                        Submit
                    </button>       
                </div>
            </div>
        </form>
    )
}