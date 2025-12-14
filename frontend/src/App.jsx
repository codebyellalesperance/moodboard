import { useState } from 'react'
import { ThemeProvider } from './context/ThemeContext'
import Header from './components/Header'
import ImageUploader from './components/ImageUploader'
import PromptInput from './components/PromptInput'
import SubmitButton from './components/SubmitButton'
import MoodSummary from './components/MoodSummary'
import ProductGrid from './components/ProductGrid'
import LoadingOverlay from './components/LoadingOverlay'
import ErrorMessage from './components/ErrorMessage'
import { getMoodcheck } from './utils/api'
import { ArrowLeft, Sparkles } from 'lucide-react'

function AppContent() {
  const [images, setImages] = useState([])
  const [prompt, setPrompt] = useState('')
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)
  const [error, setError] = useState(null)

  // Check if we have enough input to submit (images OR prompt)
  const canSubmit = images.length > 0 || prompt.trim().length > 0

  const handleSubmit = async () => {
    setLoading(true)
    setError(null)

    try {
      const data = await getMoodcheck(images, prompt)
      setResults({
        mood: data.vibe,
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
      <div className="min-h-screen pb-32 relative overflow-hidden">
        {/* Decorative orbs */}
        <div className="orb orb-1" />
        <div className="orb orb-2" />
        <div className="orb orb-3" />

        <div className="max-w-[1300px] mx-auto px-8 lg:px-16 relative z-10">
          <Header />

          <main className="mt-16 space-y-24 animate-slide-up">
            <MoodSummary mood={results.mood} />

            <div className="space-y-12">
              <div className="text-center">
                <div className="inline-flex items-center gap-3 px-5 py-2.5 rounded-full glass">
                  <Sparkles className="w-4 h-4 theme-text-secondary" />
                  <span className="text-xs font-medium tracking-[0.2em] theme-text-secondary uppercase">
                    Curated For You
                  </span>
                </div>
              </div>
              <ProductGrid products={results.products} />
            </div>

            <div className="max-w-sm mx-auto pt-8">
              <button
                onClick={handleStartOver}
                className="w-full py-5 rounded-2xl glass-card glass-hover
                           theme-text-secondary hover:theme-text-primary
                           font-medium tracking-[0.15em] uppercase text-xs
                           flex items-center justify-center gap-3"
              >
                <ArrowLeft className="w-4 h-4" />
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
    <div className="min-h-screen pb-32 flex flex-col relative overflow-hidden">
      {loading && <LoadingOverlay />}

      {/* Decorative orbs */}
      <div className="orb orb-1" />
      <div className="orb orb-2" />
      <div className="orb orb-3" />

      <div className="w-full max-w-[900px] mx-auto px-8 lg:px-12 flex-1 flex flex-col relative z-10">
        <Header />

        <main className="flex-1 flex flex-col justify-center py-12">
          {/* Hero section */}
          <div className="text-center mb-12 animate-fade-in">
            <h2 className="text-4xl md:text-5xl font-extralight tracking-tight theme-text-primary mb-4">
              Shop Your Vibe
            </h2>
            <p className="text-base theme-text-secondary font-light max-w-lg mx-auto leading-relaxed">
              Upload inspiration images, describe your aesthetic, or both — and discover products that match your style
            </p>
          </div>

          <div className="space-y-8">
            {/* Prompt Input - Now more prominent */}
            <div className="animate-slide-up opacity-0" style={{ animationDelay: '0.1s', animationFillMode: 'forwards' }}>
              <PromptInput prompt={prompt} setPrompt={setPrompt} />
            </div>

            {/* Divider */}
            <div className="flex items-center gap-4 animate-fade-in opacity-0" style={{ animationDelay: '0.2s', animationFillMode: 'forwards' }}>
              <div className="flex-1 h-px bg-gradient-to-r from-transparent via-[var(--glass-border)] to-transparent" />
              <span className="text-xs theme-text-tertiary uppercase tracking-widest">and / or</span>
              <div className="flex-1 h-px bg-gradient-to-r from-transparent via-[var(--glass-border)] to-transparent" />
            </div>

            {/* Image Uploader */}
            <div className="animate-slide-up opacity-0" style={{ animationDelay: '0.25s', animationFillMode: 'forwards' }}>
              <ImageUploader images={images} setImages={setImages} />
            </div>

            {/* Error and Submit */}
            <div className="space-y-6 animate-slide-up opacity-0" style={{ animationDelay: '0.4s', animationFillMode: 'forwards' }}>
              {error && (
                <ErrorMessage
                  message={error}
                  onRetry={() => setError(null)}
                />
              )}

              <SubmitButton
                disabled={!canSubmit}
                onClick={handleSubmit}
                loading={loading}
              />

              {!canSubmit && (
                <p className="text-center text-xs theme-text-tertiary">
                  Describe your vibe or upload at least one image to continue
                </p>
              )}
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}

function App() {
  return (
    <ThemeProvider>
      <AppContent />
    </ThemeProvider>
  )
}

export default App
