import React from "react"

import Header from "./components/Header"
import Title from "./components/Title"
import Input from "./components/Input"

export default function App(){

    const bottomEl = React.useRef(null);

    const scrollToBottom = () => {
        bottomEl?.current?.scrollIntoView({ behavior: 'smooth' });
    };

    return(
        <div className>
            <Header/>
            <Title/>

            <button onClick = {scrollToBottom} className="start">Let's get started!</button>
            <div ref={bottomEl}>
                <Input/>
            </div>
        </div>

        
    )
}

