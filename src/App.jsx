import { useState } from 'react'
import Header from './components/Header'
import ImageUploader from './components/ImageUploader'
import PromptInput from './components/PromptInput'
import SubmitButton from './components/SubmitButton'
import MoodSummary from './components/MoodSummary'
import ProductGrid from './components/ProductGrid'
import LoadingOverlay from './components/LoadingOverlay'
import ErrorMessage from './components/ErrorMessage'
import { getMoodcheck } from './utils/api'

function App() {
  const [images, setImages] = useState([])
  const [prompt, setPrompt] = useState('')
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)
  const [error, setError] = useState(null)

  const handleSubmit = async () => {
    setLoading(true)
    setError(null)

    try {
      const data = await getMoodcheck(images, prompt)
      setResults({
        mood: data.vibe,      // API returns "vibe" key
        products: data.products
      })
    } catch (err) {
      console.error('API Error:', err)
      setError(err.message || 'Something went wrong. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleStartOver = () => {
    setImages([])
    setPrompt('')
    setResults(null)
    setError(null)
  }

  // Results view
  if (results) {
    return (
      <div className="min-h-screen bg-gray-50 pb-20">
        <div className="max-w-4xl mx-auto px-4">
          <Header />

          <main className="mt-8 space-y-8">
            <MoodSummary mood={results.mood} />

            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-4">
                Shop the look
              </h3>
              <ProductGrid products={results.products} />
            </div>

            <button
              onClick={handleStartOver}
              className="w-full py-3 rounded-xl border border-gray-200 text-gray-600 
                         hover:bg-gray-50 transition-colors font-medium"
            >
              ← Start Over
            </button>
          </main>
        </div>
      </div>
    )
  }

  // Upload view
  return (
    <div className="min-h-screen bg-gray-50 pb-20">
      {loading && <LoadingOverlay />}

      <div className="max-w-2xl mx-auto px-4">
        <Header />

        <main className="mt-8 space-y-6">
          <ImageUploader images={images} setImages={setImages} />
          <PromptInput prompt={prompt} setPrompt={setPrompt} />

          {error && (
            <ErrorMessage
              message={error}
              onRetry={() => setError(null)}
            />
          )}

          <SubmitButton
            disabled={images.length === 0}
            onClick={handleSubmit}
            loading={loading}
          />

          {/* Helper text */}
          <p className="text-center text-gray-400 text-sm">
            Upload screenshots, Pinterest images, or outfit inspo to find similar products
          </p>
        </main>
      </div>
    </div>
  )
}

export default App
