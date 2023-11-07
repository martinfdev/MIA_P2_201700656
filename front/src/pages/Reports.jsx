import { useState, useEffect } from 'react'
import { useNavigate } from "react-router-dom"
import Card from '../components/Card'


function Reports() {
    const [dataImages, setDataImages] = useState([])
    useEffect(() => {
        async function fetchData() {
            try {
                const response = await fetch('http://3.89.186.159:5000/reports')
                const data = await response.json()
                setDataImages(data)
            } catch (error) {
                console.error("error to get data images", error)
            }
        }
        fetchData()
    }, [])

    const navigate = useNavigate();

    const handleBack = () => {
        navigate('/login')
    }

    const chunkArray = (myArray, chunk_size) => {
        const chunkArray = []
        for (let i = 0; i < myArray.length; i += chunk_size) {
            chunkArray.push(myArray.slice(i, i + chunk_size))
        }
        return chunkArray
    }
    //div for each 6 groups card
    //<div className="flex flex-row gap-6 p-6 justify-between items-center"></div>
    return (
        <>
            <div className="flex flex-col h-12 p-2 ">
                <div className="flex flex-row gap-8">
                    <button className="absolute top-5 right-5 p-3 rounded-md text-slate-900 font-bold bg-slate-200 border-4 hover:border-primary bg-opacity-50 hover:bg-opacity-100"
                        onClick={handleBack}
                    >Regresar</button>
                </div>
            </div>
            <div className='h-full'>
                {chunkArray(dataImages, 5).map((chunk, index) => (
                    <div key={index} className="flex flex-row gap-12 p-10 justify-between items-center">
                        {chunk.map((image, index) => (
                            <Card key={index} name={image.name} imageUrl={image.url
                            } />
                        ))}
                    </div>
                ))
                }
            </div>
        </>
    )
}

export default Reports