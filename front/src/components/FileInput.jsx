import { useRef } from 'react';
import { PropTypes } from 'prop-types';


function FileInput({ onFileContent, onFileName}) {
    const fileInput = useRef(null);

    const handleButtonClick = () => {
        fileInput.current.click()
    };

    const handleFileSelect = (e) => {
        const selectedFile = e.target.files[0];

        if (selectedFile) {
            if (selectedFile.type === "text/plain" || selectedFile.type === "") {
                const reader = new FileReader()
                reader.onload = (event) => {
                    const fileContent = event.target.result;
                    onFileContent(fileContent)
                    onFileName(selectedFile.name)
                }
                reader.readAsText(selectedFile)
            } else {
                console.log("File type not supported")
                return
            }
        }
    }

    return (
        <>
            <input
                type="file"
                accept='.txt, .adsj'
                ref={fileInput}
                className="hidden"
                onChange={handleFileSelect}
            />
            <button
                className="w-1/4 h-10 rounded-sm bg-slate-500 text-white font-bold border-2 hover:border-primary"
                onClick={handleButtonClick}>Examinar</button>
        </>
    );
}

FileInput.propTypes = {
    onFileContent: PropTypes.func.isRequired,
    onFileName: PropTypes.func.isRequired
}
export default FileInput;