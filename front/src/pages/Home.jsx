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
        setOutput(fileContent)
    }

    return (
        <div className="flex flex-col h-screen w-screen gap-5 p-2 ">
            <Header />
            <div className="flex flex-row gap-3">
                <input name="filename" type="text" defaultValue={fileName} className="w-4/5 h-10 hover:border-danger rounded-sm px-4 py-2" />
                <FileInput onFileContent={setFileContent} onFileName={setFileName} />
                <button
                    className="w-1/4 h-10 rounded-sm bg-slate-500 text-white font-bold border-2 hover:border-danger"
                    onClick={handleOutputChange}
                >Ejecutar</button>
            </div>
            <TextArea value={fileContent} onChange={handleTextChange} isEditable={true} />
            <TextArea value={output} onChange={handleTextChange} isEditable={false} />
        </div>
    );
}
export default Home;