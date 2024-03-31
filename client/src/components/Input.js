import React from "react"

export default function Input(){
    return(
        <div className="input-body">
            <div className="input-grid">

                <div class="pdf">
                    <p>Supported file types: .pdf, .doc</p>
                    <label for="formFileMultiple" className="form-label">Browse files</label>
                    <input type="file" id="formFileMultiple" multiple/>
                </div>

                
        
        
                <div class="dropdown">
                    <button class="btn btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                        Dropdown button
                    </button>
                    <ul class="dropdown-menu">
                        <li><a class="dropdown-item" href="#">Sample Qns</a></li>
                        <li><a class="dropdown-item" href="#">Content</a></li>
                    </ul>


                    <input class="btn btn-primary" type="submit" value="Submit"/>

                </div>
            

            </div>

            
        </div>
    )
}