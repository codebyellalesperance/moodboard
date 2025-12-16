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
  const [displayedCount, setDisplayedCount] = useState(20)

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
      // Pre-select item type filter if backend detected one
      if (data.detected_item_type) {
        setFilters(prev => ({
          ...prev,
          itemTypes: [data.detected_item_type]
        }))
      }
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
    setDisplayedCount(20)
  }

  const handleLoadMore = () => {
    setDisplayedCount(prev => prev + 20)
  }

  const [isReloadingFilter, setIsReloadingFilter] = useState(false)

  const handleReloadWithFilter = async (category, retailer) => {
    if (!results?.mood?.name) return

    setIsReloadingFilter(true)
    try {
      const filterPrompt = category
        ? `${results.mood.name} style ${category.toLowerCase()}`
        : `${results.mood.name} from ${retailer}`

      const data = await getMoodcheck([], filterPrompt, { maxProducts: 50 })
      setResults(prev => ({ ...prev, products: data.products }))
      setFilters(DEFAULT_FILTERS)
      setDisplayedCount(20)
    } catch (err) {
      console.error('Reload error:', err)
    } finally {
      setIsReloadingFilter(false)
    }
  }

  // Results View
  if (results) {
    return (
      <div className="min-h-screen p-3 sm:p-4 md:p-6 relative">
        <Header />

        <main className="grid grid-cols-1 lg:grid-cols-12 gap-6 lg:gap-8 max-w-[1400px] mx-auto">
          {/* Main Editorial Content */}
          <div className="lg:col-span-9 animate-fade-in lg:pr-6">
            <div className="flex justify-between items-end mb-4 sm:mb-6 border-b border-[var(--border-color)] pb-2">
              <h2 className="font-serif text-2xl sm:text-3xl italic">Curated Selection</h2>
              <div className="flex items-center gap-3 sm:gap-6 mb-1">
                <span className="font-mono text-[10px] sm:text-xs">{filteredProducts.length} ITEMS</span>
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
              <div className="h-64 flex flex-col items-center justify-center border border-[var(--border-color)]">
                <div className="w-4 h-4 bg-[var(--color-text-primary)] animate-spin mb-4" />
                <span className="font-mono text-xs tracking-widest uppercase">Curating new collection...</span>
              </div>
            ) : (
              <ProductGrid
                products={filteredProducts}
                displayedCount={displayedCount}
                onLoadMore={handleLoadMore}
              />
            )}
          </div>

          {/* Sidebar / Info Column */}
          <div className="lg:col-span-3 space-y-6 sm:space-y-8 animate-slide-up order-first lg:order-last">
            <div className="sticky top-4">
              <button onClick={handleStartOver} className="mb-4 sm:mb-6 flex items-center gap-2 text-xs font-mono uppercase tracking-widest hover:underline hover-invert px-3 py-1.5 border border-transparent hover:border-[var(--color-text-primary)] transition-all">
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
    <div className="min-h-screen p-3 sm:p-4 md:p-6 lg:p-8 relative flex flex-col">
      {loading && <LoadingOverlay />}
      <Header />

      <main className="flex-1 flex flex-col items-center justify-center relative max-w-[1200px] mx-auto w-full py-4 sm:py-6">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 sm:gap-8 lg:gap-12 w-full items-center">

          {/* Left: Text & Prompt */}
          <div className="space-y-6 sm:space-y-8 lg:space-y-10 order-2 lg:order-1">
            <div className="animate-slide-up">
              <span className="font-mono text-[10px] sm:text-xs tracking-[0.2em] sm:tracking-[0.3em] uppercase opacity-70 mb-2 sm:mb-3 block">The AI Stylist</span>
              <h2 className="font-serif text-4xl sm:text-5xl md:text-6xl lg:text-7xl leading-[0.9] mb-4 sm:mb-6">
                Define <br className="hidden sm:block" /> Your <span className="italic">Style</span>
              </h2>
              <p className="font-mono text-xs sm:text-sm max-w-md border-l border-[var(--border-color)] pl-4 sm:pl-6 py-2 opacity-80">
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
          <div className="relative animate-slide-in-right order-1 lg:order-2">
            <div className="relative z-10">
              <div className="absolute -top-4 -left-4 sm:-top-6 sm:-left-6 hidden sm:block">
                <Plus className="w-3 h-3 sm:w-4 sm:h-4 text-[var(--color-text-primary)] opacity-50" />
              </div>
              <div className="absolute -bottom-4 -right-4 sm:-bottom-6 sm:-right-6 hidden sm:block">
                <Plus className="w-3 h-3 sm:w-4 sm:h-4 text-[var(--color-text-primary)] opacity-50" />
              </div>

              <ImageUploader images={images} setImages={setImages} />

              <div className="mt-4 sm:mt-6">
                {error && <ErrorMessage message={error} onRetry={() => setError(null)} />}
                <SubmitButton disabled={!canSubmit} onClick={handleSubmit} loading={loading} />
              </div>
            </div>

            {/* Decorative BG Grid */}
            <div className="absolute inset-0 border border-[var(--border-color)] opacity-20 -z-10 translate-x-2 translate-y-2 sm:translate-x-4 sm:translate-y-4 hidden sm:block" />
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
