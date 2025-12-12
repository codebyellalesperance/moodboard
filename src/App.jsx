import Header from './components/Header'
import ImageUploader from './components/ImageUploader'

function App() {
  return (
    <div className="min-h-screen bg-gray-50 pb-20">
      <div className="max-w-2xl mx-auto px-4">
        <Header />

        <main className="mt-8">
          <ImageUploader />
        </main>
      </div>
    </div>
  )
}

export default App
