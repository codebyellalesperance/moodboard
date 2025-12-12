import { useState } from 'react'
import Header from './components/Header'
import ImageUploader from './components/ImageUploader'
import PromptInput from './components/PromptInput'

function App() {
  const [images, setImages] = useState([])
  const [prompt, setPrompt] = useState('')

  return (
    <div className="min-h-screen bg-gray-50 pb-20">
      <div className="max-w-2xl mx-auto px-4">
        <Header />

        <main className="mt-8 space-y-6">
          <ImageUploader images={images} setImages={setImages} />
          <PromptInput prompt={prompt} setPrompt={setPrompt} />
        </main>
      </div>
    </div>
  )
}

export default App
