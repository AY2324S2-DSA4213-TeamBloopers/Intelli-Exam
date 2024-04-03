import React from "react"

export default function InputFile(props){
    return(
        <div>
            

            <div class="file">
                <div>
                    {props.files.length === 0 && <p>Supported file types: .pdf, .doc</p>}
                    <label 
                        htmlFor="formFileMultiple" 
                        className= {props.files.length === 0 ? "form-label" : "add"} >
                        {props.files.length === 0 ? "Browse files" : "Add files"}
                    </label>
                    <input 
                        type="file" 
                        id="formFileMultiple" 
                        multiple
                        onChange={props.upload}
                        name="file"/>
                    <div>
                        {props.files.map((file, index) =>{
                            return(
                            <div className="delete" key={index}>
                                <span>{file.name}</span>

                                <button 
                                    type= "button" 
                                    onClick={() => props.delete(index)}
                                    >
                                X
                                </button>
                            </div>
                            )
                        })}
                    </div>

                </div>
            </div>
        </div>
        
    )
}