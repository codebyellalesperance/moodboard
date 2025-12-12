import { useRef } from 'react'
import { Upload, X, Image as ImageIcon } from 'lucide-react'

function ImageUploader({ images, setImages }) {
    const fileInputRef = useRef(null)

    const handleFileSelect = (e) => {
        const files = Array.from(e.target.files)
        processFiles(files)
    }

    const handleDrop = (e) => {
        e.preventDefault()
        const files = Array.from(e.dataTransfer.files)
        processFiles(files)
    }

    const processFiles = (files) => {
        const validFiles = files.filter(file =>
            file.type.startsWith('image/') && file.size <= 5 * 1024 * 1024
        )

        if (images.length + validFiles.length > 5) {
            alert('Max 5 images allowed')
            return
        }

        setImages(prev => [...prev, ...validFiles])
    }

    const removeImage = (index) => {
        setImages(prev => prev.filter((_, i) => i !== index))
    }

    return (
        <div className="space-y-6">
            <div
                onClick={() => fileInputRef.current?.click()}
                onDragOver={(e) => e.preventDefault()}
                onDrop={handleDrop}
                className="glass glass-hover rounded-3xl p-16 text-center cursor-pointer 
                   transition-all duration-500 group min-h-[320px] flex flex-col 
                   items-center justify-center border-dashed border-white/20 hover:border-white/40"
            >
                <input
                    type="file"
                    ref={fileInputRef}
                    onChange={handleFileSelect}
                    className="hidden"
                    accept="image/*"
                    multiple
                />

                <div className="w-16 h-16 rounded-full bg-white/5 flex items-center justify-center 
                        group-hover:bg-white/10 transition-colors mb-6 backdrop-blur-md">
                    <Upload className="w-6 h-6 text-white/60" />
                </div>

                <p className="text-sm font-light tracking-[0.2em] text-white/80 uppercase">
                    Drop Images
                </p>
            </div>

            {images.length > 0 && (
                <div className="grid grid-cols-5 gap-3">
                    {images.map((file, index) => (
                        <div key={index} className="relative aspect-square group">
                            <img
                                src={URL.createObjectURL(file)}
                                alt={`Upload ${index + 1}`}
                                className="w-full h-full object-cover rounded-lg border border-white/10"
                            />
                            <button
                                onClick={() => removeImage(index)}
                                className="absolute -top-2 -right-2 p-1 bg-black/80 text-white/60 
                           hover:text-white rounded-full opacity-0 group-hover:opacity-100 
                           transition-opacity border border-white/10"
                            >
                                <X className="w-3 h-3" />
                            </button>
                        </div>
                    ))}
                </div>
            )}
        </div>
    )
}

export default ImageUploader
