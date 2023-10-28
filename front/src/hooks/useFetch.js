import { useState, useEffect } from 'react'

export default function useFetch(endpoint) {
    const [data, setData] = useState(null)

    useEffect(() => {
        (async () => {
            try {
                const response = await fetch(endpoint)
                const data = await response.json()
                setData(data)
            } catch (error) {
                console.error(error)
            }
        })()
    }, [endpoint])
    return [data]
}