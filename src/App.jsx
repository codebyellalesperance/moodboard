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
import { ArrowLeft } from 'lucide-react'

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
      setError(err.message || 'Analysis failed')
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
      <div className="min-h-screen pb-20">
        <div className="max-w-[1400px] mx-auto px-6 lg:px-12">
          <Header />

          <main className="mt-8 space-y-16">
            <MoodSummary mood={results.mood} />

            <div className="space-y-8">
              <h3 className="text-xs font-medium tracking-[0.2em] text-white/40 uppercase text-center">
                Curated For You
              </h3>
              <ProductGrid products={results.products} />
            </div>

            <div className="max-w-md mx-auto">
              <button
                onClick={handleStartOver}
                className="w-full py-4 rounded-xl border border-white/10 text-white/40 
                           hover:bg-white/5 hover:text-white transition-all 
                           font-light tracking-widest uppercase text-xs flex items-center justify-center gap-2"
              >
                <ArrowLeft className="w-3 h-3" />
                Start Over
              </button>
            </div>
          </main>
        </div>
      </div>
    )
  }

  // Upload view
  return (
    <div className="min-h-screen pb-20 flex flex-col">
      {loading && <LoadingOverlay />}

      <div className="w-full max-w-[1200px] mx-auto px-6 lg:px-12 flex-1 flex flex-col">
        <Header />

        <main className="mt-8 lg:mt-16 flex-1 flex flex-col justify-center max-w-3xl mx-auto w-full space-y-10">
          <ImageUploader images={images} setImages={setImages} />

          <div className="space-y-10">
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
          </div>
        </main>
      </div>
    </div>
  )
}

export default App
