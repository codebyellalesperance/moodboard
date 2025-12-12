import { useState, useEffect } from 'react'

function Clock() {
    const [time, setTime] = useState(new Date())

    useEffect(() => {
        const timer = setInterval(() => {
            setTime(new Date())
        }, 1000)

        return () => clearInterval(timer)
    }, [])

    const formatTime = (date) => {
        return date.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            hour12: true
        })
    }

    return (
        <div className="font-light tracking-widest text-sm theme-text-secondary tabular-nums">
            {formatTime(time)}
        </div>
    )
}

export default Clock
