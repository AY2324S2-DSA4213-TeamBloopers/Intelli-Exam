import React from "react"
import InputFile from "./InputFile"
import Dropdown from "./Dropdown"


// import axios from "axios"

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

    
    function handleSubmit(event){

        event.preventDefault();
        /*
        
        if (!files){
            return;
        }

        const fd = new FormData()
        files.forEach((file, index) => {
            fd.append(`file${index+1}`, file)
        })
        

        axios.post("", fd, {
        })*/
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