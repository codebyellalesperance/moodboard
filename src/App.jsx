import { useState } from 'react'
import Header from './components/Header'
import ImageUploader from './components/ImageUploader'

function App() {
  const [images, setImages] = useState([])

  return (
    <div className="min-h-screen bg-gray-50 pb-20">
      <div className="max-w-2xl mx-auto px-4">
        <Header />

        <main className="mt-8">
          <ImageUploader images={images} setImages={setImages} />

          {/* Debug: show image count */}
          <p className="mt-4 text-center text-gray-400 text-sm">
            {images.length} image(s) selected
          </p>
        </main>
      </div>
    </div>
  )
}

export default App
