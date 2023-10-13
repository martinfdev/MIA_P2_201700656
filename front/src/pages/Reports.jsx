import { useState, useEffect } from 'react'
import Card from '../components/Card'

function Reports() {
    const [dataImages, setDataImages] = useState([])
    useEffect(() => {
        async function fetchData() {
            try {
                const response = await fetch('https://picsum.photos/v2/list?page=2&limit=100')
                const data = await response.json()
                setDataImages(data)
            } catch (error) {
                console.error("error to get data images", error)
            }
        }
        fetchData()
    }, [])

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
        <div className='h-screen'>
            {chunkArray(dataImages, 5).map((chunk, index) => (
                <div key={index} className="flex flex-row gap-12 p-10 justify-between items-center">
                    {chunk.map((image, index) => (
                        <Card key={index} name={image.author} imageUrl={image.download_url
                        } />
                    ))}
                </div>
            ))
            }
        </div>
    )
}

export default Reports