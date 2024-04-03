import React from "react"

export default function Title(){
    return(
        <div className="title-box">
            <div className="title">
                <h1>Stuck on generating exam Q&As?</h1>
                <span>
                    Intelli-Exam uses LLMs to generate user-specific exam Q&As
                </span>

                <div className="credits" href= "https://www.pexels.com/photo/a-person-marking-a-test-paper-6684373/">
                    <img src="images/circle.svg"/>
                    <span>Andy Barbour, Pexels</span>
                </div>
            </div>            
        </div>
        
    )
}