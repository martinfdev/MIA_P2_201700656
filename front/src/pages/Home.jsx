import { useState } from 'react';
import FileInput from '../components/FileInput';
import TextArea from '../components/TextArea';
import Header from '../components/Header';


function Home() {
    const [fileContent, setFileContent] = useState("")
    const [fileName, setFileName] = useState(null)
    const [output, setOutput] = useState("Salida>>")

    const handleTextChange = (newText) => {
        setFileContent(newText)
    }

    const handleOutputChange = () => {
        fetch('http://3.89.186.159:5000/execute', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "content": fileContent
            })
        }).then(res => res.json())
            .then(data => {
                var output_console = data.output
                var string_output_console = ""
                for (let i = 0; i < output_console.length; i++) {
                    string_output_console += output_console[i] + "\n"
                }
                setOutput(string_output_console)
            }).catch(err => console.log(err))
    }

    const handleCleanTextArea = () => {
        setFileContent("")
        setOutput("Salida>>")
        // window.location.reload(false)
    }


    return (
        <div className="flex flex-col h-screen w-screen gap-3 p-2 ">
            <Header />
            <div className="flex flex-row gap-8">
                <input name="filename" type="text" defaultValue={fileName} className="w-4/5 h-10 hover:border-danger rounded-sm px-4 py-2" />
                <FileInput onFileContent={setFileContent} onFileName={setFileName} />
                <button
                    className="w-1/4 h-10 rounded-sm bg-slate-500 text-white font-bold border-2 hover:border-danger"
                    onClick={handleOutputChange}
                >Ejecutar</button>
                <button className="w-1/4 h-10 rounded-sm bg-slate-500 text-white font-bold border-2 hover:border-danger"
                    onClick={handleCleanTextArea}
                >Limpiar</button>
            </div>
            <TextArea value={fileContent} onChange={handleTextChange} isEditable={true} />
            <TextArea value={output} onChange={handleTextChange} isEditable={false} />
        </div>
    );
}
export default Home;