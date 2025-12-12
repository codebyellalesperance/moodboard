import { useState } from 'react'
import Header from './components/Header'
import ImageUploader from './components/ImageUploader'
import PromptInput from './components/PromptInput'
import SubmitButton from './components/SubmitButton'
import MoodSummary from './components/MoodSummary'
import ProductGrid from './components/ProductGrid'

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

const MOCK_PRODUCTS = [
  {
    id: "ss_1",
    name: "Oversized Linen Blazer",
    brand: "Vince",
    price: 89.99,
    original_price: 145.00,
    on_sale: true,
    image_url: "https://placehold.co/400x400/f5f5dc/333?text=Blazer",
    product_url: "https://example.com/product1",
    retailer: "Nordstrom"
  },
  {
    id: "ss_2",
    name: "Ribbed Cotton Tank",
    brand: "Everlane",
    price: 28.00,
    original_price: 28.00,
    on_sale: false,
    image_url: "https://placehold.co/400x400/ffffff/333?text=Tank",
    product_url: "https://example.com/product2",
    retailer: "Everlane"
  },
  {
    id: "ss_3",
    name: "Wide Leg Trousers",
    brand: "COS",
    price: 115.00,
    original_price: 115.00,
    on_sale: false,
    image_url: "https://placehold.co/400x400/c19a6b/fff?text=Trousers",
    product_url: "https://example.com/product3",
    retailer: "COS"
  },
  {
    id: "ss_4",
    name: "Gold Hoop Earrings",
    brand: "Mejuri",
    price: 48.00,
    original_price: 65.00,
    on_sale: true,
    image_url: "https://placehold.co/400x400/ffd700/333?text=Hoops",
    product_url: "https://example.com/product4",
    retailer: "Mejuri"
  },
]

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
      setResults({ mood: MOCK_MOOD, products: MOCK_PRODUCTS })
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

            <ProductGrid products={results.products} />

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
