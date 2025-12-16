import { useState, useMemo } from 'react'
import { ThemeProvider } from './context/ThemeContext'
import Header from './components/Header'
import ImageUploader from './components/ImageUploader'
import PromptInput from './components/PromptInput'
import SubmitButton from './components/SubmitButton'
import MoodSummary from './components/MoodSummary'
import ProductGrid from './components/ProductGrid'
import ProductFilters, { filterProducts, DEFAULT_FILTERS } from './components/ProductFilters'
import LoadingOverlay from './components/LoadingOverlay'
import ErrorMessage from './components/ErrorMessage'
import { getMoodcheck } from './utils/api'
import { ArrowLeft, Plus } from 'lucide-react'

function AppContent() {
  const [images, setImages] = useState([])
  const [prompt, setPrompt] = useState('')
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)
  const [error, setError] = useState(null)
  const [filters, setFilters] = useState(DEFAULT_FILTERS)

  const canSubmit = images.length > 0 || prompt.trim().length > 0

  const filteredProducts = useMemo(() => {
    if (!results?.products) return []
    return filterProducts(results.products, filters)
  }, [results?.products, filters])

  const handleSubmit = async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await getMoodcheck(images, prompt)
      setResults({
        mood: data.vibe,
        trend: data.trend,
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
    setFilters(DEFAULT_FILTERS)
  }

  const [isReloadingFilter, setIsReloadingFilter] = useState(false)

  const handleReloadWithFilter = async (category, retailer) => {
    if (!results?.mood?.name) return

    setIsReloadingFilter(true)
    try {
      const filterPrompt = category
        ? `${results.mood.name} style ${category.toLowerCase()}`
        : `${results.mood.name} from ${retailer}`

      const data = await getMoodcheck([], filterPrompt, { maxProducts: 30 })
      setResults(prev => ({ ...prev, products: data.products }))
      setFilters(DEFAULT_FILTERS)
    } catch (err) {
      console.error('Reload error:', err)
    } finally {
      setIsReloadingFilter(false)
    }
  }

  // Results View
  if (results) {
    return (
      <div className="min-h-screen p-4 md:p-8 relative">
        <Header />

        <main className="magazine-grid max-w-[1600px] mx-auto">
          {/* Main Editorial Content */}
          <div className="col-span-12 lg:col-span-9 animate-fade-in pr-0 lg:pr-8">
            <div className="flex justify-between items-end mb-8 border-b border-[var(--border-color)] pb-2">
              <h2 className="font-serif text-4xl italic">Curated Selection</h2>
              <div className="flex items-center gap-6 mb-1">
                <span className="font-mono text-xs">{filteredProducts.length} ITEMS FOUND</span>
                <ProductFilters
                  products={results.products}
                  filters={filters}
                  setFilters={setFilters}
                  onReloadWithFilter={handleReloadWithFilter}
                  isReloading={isReloadingFilter}
                />
              </div>
            </div>

            {isReloadingFilter ? (
              <div className="h-96 flex flex-col items-center justify-center border border-[var(--border-color)]">
                <div className="w-4 h-4 bg-[var(--color-text-primary)] animate-spin mb-4" />
                <span className="font-mono text-xs tracking-widest uppercase">Curating new collection...</span>
              </div>
            ) : (
              <ProductGrid products={filteredProducts} />
            )}
          </div>

          {/* Sidebar / Info Column (Now on Right) */}
          <div className="col-span-12 lg:col-span-3 space-y-12 animate-slide-up order-first lg:order-last">
            <div className="sticky top-8">
              <button onClick={handleStartOver} className="mb-8 flex items-center gap-2 text-xs font-mono uppercase tracking-widest hover:underline hover-invert px-4 py-2 border border-transparent hover:border-[var(--color-text-primary)] transition-all">
                <ArrowLeft className="w-3 h-3" /> Back to Edit
              </button>

              <MoodSummary mood={results.mood} trend={results.trend} />
            </div>
          </div>
        </main>
      </div>
    )
  }

  // Input View (Landing)
  return (
    <div className="min-h-screen p-4 md:p-8 relative flex flex-col">
      {loading && <LoadingOverlay />}
      <Header />

      <main className="flex-1 flex flex-col items-center justify-center relative max-w-[1400px] mx-auto w-full">
        <div className="magazine-grid w-full items-center">

          {/* Left: Text & Prompt */}
          <div className="col-span-12 lg:col-span-6 space-y-12 pr-0 lg:pr-12">
            <div className="animate-slide-up">
              <span className="font-mono text-xs tracking-[0.3em] uppercase opacity-70 mb-4 block">The AI Stylist</span>
              <h2 className="font-serif text-6xl md:text-8xl leading-[0.9] mb-8">
                Define <br /> Your <span className="italic">Style</span>
              </h2>
              <p className="font-mono text-sm max-w-md border-l border-[var(--border-color)] pl-6 py-2 opacity-80">
                Upload your inspiration or describe the vision. Our AI curates a high-fashion editorial just for you.
              </p>
            </div>

            <div className="animate-slide-up" style={{ animationDelay: '0.1s' }}>
              <PromptInput
                prompt={prompt}
                setPrompt={setPrompt}
                onSubmit={handleSubmit}
                canSubmit={canSubmit && !loading}
              />
            </div>
          </div>

          {/* Right: Upload & Actions */}
          <div className="col-span-12 lg:col-span-6 mt-12 lg:mt-0 relative animate-slide-in-right">
            <div className="relative z-10">
              <div className="absolute -top-6 -left-6">
                <Plus className="w-4 h-4 text-[var(--color-text-primary)] opacity-50" />
              </div>
              <div className="absolute -bottom-6 -right-6">
                <Plus className="w-4 h-4 text-[var(--color-text-primary)] opacity-50" />
              </div>

              <ImageUploader images={images} setImages={setImages} />

              <div className="mt-8">
                {error && <ErrorMessage message={error} onRetry={() => setError(null)} />}
                <SubmitButton disabled={!canSubmit} onClick={handleSubmit} loading={loading} />
              </div>
            </div>

            {/* Decorative BG Grid */}
            <div className="absolute inset-0 border border-[var(--border-color)] opacity-20 -z-10 translate-x-4 translate-y-4" />
          </div>
        </div>
      </main>
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
