import React from "react"

export default function Header(){
    return(
        <div className="header">
            <div className="header--team">
                <div className="header--brand">
                    <span>TeamBloopers</span>
                    <img src= "images/Picture1.png"/>
                </div>
                
                <span>DSA4213 Project</span>
                                
            </div>

            <img className="logo" src = "images/logo.png"/>
            
            <div className="icons">
                <img className= "search" src="images/search.svg"/>
                <img className= "user" src="images/person-circle.svg"/>
            </div>
            
            
        </div>
    )
}