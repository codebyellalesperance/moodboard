import { useState } from 'react'
import Header from './components/Header'
import ImageUploader from './components/ImageUploader'
import PromptInput from './components/PromptInput'
import SubmitButton from './components/SubmitButton'

function App() {
  const [images, setImages] = useState([])
  const [prompt, setPrompt] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = () => {
    console.log('Submitting:', { images, prompt })
    // TODO: Wire up API in later step

    // Simulate loading for now
    setLoading(true)
    setTimeout(() => {
      setLoading(false)
      alert('API will be connected in a later step!')
    }, 2000)
  }

  return (
    <div className="min-h-screen bg-gray-50 pb-20">
      <div className="max-w-2xl mx-auto px-4">
        <Header />

        <main className="mt-8 space-y-6">
          <ImageUploader images={images} setImages={setImages} />
          <PromptInput prompt={prompt} setPrompt={setPrompt} />
          <SubmitButton
            disabled={images.length === 0}
            onClick={handleSubmit}
            loading={loading}
          />
        </main>
      </div>
    </div>
  )
}

export default App
