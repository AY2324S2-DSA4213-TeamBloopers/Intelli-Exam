  import React, { useEffect } from "react";
  import InputFile from "./InputFile";
  import UploadType from "./UploadType";

  import axios from "axios";
  import QnNum from "./QnNum";

  export default function Input() {
    // option for type of upload
    const [opt, setOpt] = React.useState("");

    function handleOptChange(event) {
      setOpt(event.target.value);
    }

    // number of mcq & open-ended qns to be generated
    const [mcq, setMcq] = React.useState("");
    const [oe, setOe] = React.useState("");

    // check for errors
    const [error, setError] = React.useState({
      mcq: false,
      oe: false,
      all: false,
    });

    // handle updates for inputs of numbers of mcq/ oe
    function handleDecrease(event) {
      event.target.id === "mcq" ? mcq === "" && setMcq(0) : oe === "" && setOe(0);

      event.target.id === "mcq"
        ? 0 < mcq && setMcq((prev) => prev - 1)
        : 0 < oe && setOe((prev) => prev - 1);
    }

    function handleIncrease(event) {
      event.target.id === "mcq" ? mcq === "" && setMcq(0) : oe === "" && setOe(0);

      event.target.id === "mcq"
        ? mcq < 20 && setMcq((prev) => prev + 1)
        : oe < 20 && setOe((prev) => prev + 1);
    }

    function handleChange(event) {
      const { id, value } = event.target;

      const newValue = Number.isInteger(parseInt(value)) ? parseInt(value) : "";

      0 <= newValue && newValue <= 20
        ? setError((prev) => {
            return { ...prev, [id]: false };
          })
        : setError((prev) => {
            return { ...prev, [id]: true };
          });

      id === "mcq" ? setMcq(newValue) : setOe(newValue);
    }

    // for uploading of files
    const [files, setFile] = React.useState([]);

    function handleFile(event) {
      const uploadedFiles = event.target.files;
      setFile([...files, ...uploadedFiles]);
      event.target.value = null
    }

    function handleDelete(index) {
      setFile(files.toSpliced(index, 1));
    }

    // for submitting files to backend
    const sendPDFToBackend = async () => {
      setLoading(true);
      try {
        if (!files) {
          console.log("no files");
        }

        const fd = new FormData();
        files.forEach((file, index) => {
          fd.append(`file${index + 1}`, file);
        });

        const response = await axios.post(
          `http://localhost:5001/questions?module-code=DSA4213&input-type=${opt}&open-ended-count=${oe}&mcq-count=${mcq}`,
          fd,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
            responseType: "blob",
          }
        );

        const blob = new Blob([response.data], {
          type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        });

        // Create a temporary URL to the Excel file
        const url = window.URL.createObjectURL(blob);

        // Create a link and trigger the download
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", "output.xlsx");
        document.body.appendChild(link);
        link.click();

        console.log("PDF uploaded successfully:", response.data);
      } catch (error) {
        console.error("Error uploading PDF:", error);
      }
      setLoading(false);
    };

    function handleSubmit(event) {
      event.preventDefault();
      console.log(files)
      if (opt && files.length != 0 && mcq && oe) {
        setError((prev) => {
          return { ...prev, all: false };
        });

        sendPDFToBackend();
      } else {
        setError((prev) => {
          return { ...prev, all: true };
        });
      }
    }

    
    const [loading, setLoading] = React.useState(false); // Added state for loading circle
    const [mod, setMod] = React.useState("--Choose Module--"); // Added state for module selected
    const [isLegalMod, setLegalMod] = React.useState(true)// Added legality for module selected

    function handleModChange(event) { // Added mod change function
      const newValue = event.target.value;
      setMod(newValue);
    }
    useEffect(() => { // Update legality when mod changes
      setLegalMod(mod === "DSA4213" || mod === "--Choose Module--");
    }, [mod]);

    return (
      <form onSubmit={handleSubmit} className="input-body">
        <h1 className="file--title">
          Upload slides or documents of the content you teach to generate Exam
          Q&As!
        </h1>

        <div>
          <span className="module">NUS Module:</span>
          
          {!isLegalMod && (
            <span className="notice">
              Sorry, current module selection is not available
            </span>
          )}
          
          <select className="btn btn-secondary dropdown-toggle" value={mod} onChange={handleModChange}>
            <option>--Choose Module--</option>
            <option>DSA4213</option>
            <option>DSA2102</option>
            <option>DSA1101</option>
          </select>
        </div>

        <div className="input-grid">
          <InputFile
            upload={handleFile}
            delete={handleDelete}
            files={files}
            error={error}
          />

          <div class="buttons">
            <UploadType value={opt} onChange={handleOptChange} error={error}/>
            <QnNum
              mcq={mcq}
              oe={oe}
              increase={handleIncrease}
              decrease={handleDecrease}
              onChange={handleChange}
              error={error}
            />

            <button
              className="btn btn-primary"
              value="Submit"
              onChange={handleSubmit}
              disabled={loading}
            >
              {loading ? <i className="fa fa-spinner fa-spin"></i> : "Submit"}
            </button>
          </div>
        </div>
      </form>
    );
  }
