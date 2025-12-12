import { useState } from 'react'
import Header from './components/Header'
import ImageUploader from './components/ImageUploader'
import PromptInput from './components/PromptInput'
import SubmitButton from './components/SubmitButton'
import MoodSummary from './components/MoodSummary'

// Mock data for testing - will be replaced by API response
const MOCK_MOOD = {
  name: "Quiet Luxury Coastal",
  mood: "Effortless, polished, understated confidence",
  color_palette: [
    { name: "Cream", hex: "#F5F5DC" },
    { name: "Camel", hex: "#C19A6B" },
    { name: "White", hex: "#FFFFFF" },
    { name: "Navy", hex: "#1a2a4a" },
  ],
  key_pieces: [
    "Oversized linen blazer",
    "White tank",
    "Wide-leg trousers",
    "Gold hoops",
    "Leather slides"
  ]
}

function App() {
  const [images, setImages] = useState([])
  const [prompt, setPrompt] = useState('')
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)

  const handleSubmit = () => {
    setLoading(true)

    // Simulate API call with mock data
    setTimeout(() => {
      setLoading(false)
      setResults({ mood: MOCK_MOOD, products: [] })
    }, 2000)
  }

  const handleStartOver = () => {
    setImages([])
    setPrompt('')
    setResults(null)
  }

  // Show results view if we have results
  if (results) {
    return (
      <div className="min-h-screen bg-gray-50 pb-20">
        <div className="max-w-2xl mx-auto px-4">
          <Header />

          <main className="mt-8 space-y-6">
            <MoodSummary mood={results.mood} />

            {/* Products will go here in next step */}
            <p className="text-center text-gray-400">Products coming next...</p>

            <button
              onClick={handleStartOver}
              className="w-full py-3 rounded-xl border border-gray-200 text-gray-600 
                         hover:bg-gray-50 transition-colors"
            >
              Start Over
            </button>
          </main>
        </div>
      </div>
    )
  }

  // Show upload view
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
