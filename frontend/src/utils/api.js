// Convert a File to base64 data URI
const fileToBase64 = (file) => {
    return new Promise((resolve, reject) => {
        const reader = new FileReader()
        reader.readAsDataURL(file)
        reader.onload = () => resolve(reader.result)
        reader.onerror = (error) => reject(error)
    })
}

// Main API function
export async function getMoodcheck(images, prompt) {
    // Convert images to base64 (if any)
    const base64Images = images.length > 0
        ? await Promise.all(images.map(file => fileToBase64(file)))
        : []

    // API URL - update this to your backend URL
    const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001'

    const response = await fetch(`${API_URL}/api/moodcheck`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            images: base64Images,
            prompt: prompt || ''
        })
    })

    if (!response.ok) {
        const error = await response.json().catch(() => ({}))
        throw new Error(error.error || 'Failed to analyze your vibe')
    }

    const data = await response.json()

    if (!data.success) {
        throw new Error(data.error || 'Failed to analyze your vibe')
    }

    return data
}
