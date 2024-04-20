import React from "react"

export default function UploadType(props){
    return(
        <div className="upload-type">
            {!props.value && props.error.all && <span className="notice">*Required: Upload Type</span>}
            
            <select 
                onChange={props.onChange} 
                name="type"
                value={props.value}
                className="btn btn-secondary dropdown-toggle" 
                aria-expanded="false"
                >
                    
                <option value="">--Type Of Upload--</option>
                <option value="sample">Sample Questions</option>
                <option value="content">Context</option>
            </select>
            
        </div>
    )
}