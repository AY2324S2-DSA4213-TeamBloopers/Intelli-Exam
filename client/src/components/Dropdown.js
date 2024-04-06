import React from "react"

export default function Dropdown(props){
    return(
        <div className="dropdown">
            <select 
                onChange={props.onChange} 
                name="type"
                value={props.value}
                className="btn btn-secondary dropdown-toggle" 
                aria-expanded="false"
                >
                    
                <option value="">--Type Of Upload--</option>
                <option value="sample">Sample Questions</option>
                <option value="content">Content</option>
            </select>
        </div>
    )
}