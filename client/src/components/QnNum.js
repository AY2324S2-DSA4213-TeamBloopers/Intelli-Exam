import React from "react";

export default function QnNum(props) {
  return (
    <div>
      {props.error.mcq && <span className="notice">*Number must be within 0 to 20</span>}
      {props.mcq === "" && props.error.all && <span className="notice">*Required: No. of MCQs</span>}
    
      <div className="qn-grid">
        <span>Number of MCQs:</span>
        <div className="num-grid">
          <input
            id="mcq"
            type="text"
            placeholder="Max 20"
            value={props.mcq}
            onChange={props.onChange}
            className="num-input"
          ></input>

          <div className="count-buttons">
            <button
              className="down"
              type="button"
              id="mcq"
              onClick={props.increase}
            >
              V
            </button>
            <button type="button" id="mcq" onClick={props.decrease}>
              V
            </button>
          </div>
        </div>
      </div>
      {props.oe === "" && props.error.all && <span className="notice">*Required: No. of OE Qns</span>}
      {props.error.oe && <span className="notice">*Number must be within 0 to 20</span>}
      
      <div className="qn-grid">
        <span>Number of Open Ended Qns:</span>
        <div className="num-grid">
          <input
            id="oe"
            type="text"
            placeholder="Max 20"
            value={props.oe}
            onChange={props.onChange}
            className="num-input"
          ></input>
          <div className="count-buttons">
            <button
              className="down"
              type="button"
              id="oe"
              onClick={props.increase}
            >
              V
            </button>
            <button type="button" id="oe" onClick={props.decrease}>
              V
            </button>
          </div>
        </div>
      </div>
      
    </div>
  );
}
