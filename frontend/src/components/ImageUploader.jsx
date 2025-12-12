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
                className="glass-card rounded-3xl text-center cursor-pointer group
                   min-h-[280px] flex flex-col items-center justify-center
                   border-dashed border-2 border-[var(--glass-border)]
                   hover:border-[var(--glass-border-hover)] transition-all duration-500
                   relative overflow-hidden"
            >
                <input
                    type="file"
                    ref={fileInputRef}
                    onChange={handleFileSelect}
                    className="hidden"
                    accept="image/*"
                    multiple
                />

                {/* Decorative gradient on hover */}
                <div className="absolute inset-0 bg-gradient-to-br from-[var(--gradient-start)] via-transparent to-[var(--gradient-end)] opacity-0 group-hover:opacity-30 transition-opacity duration-700" />

                <div className="relative z-10 flex flex-col items-center">
                    <div className="w-16 h-16 rounded-2xl glass flex items-center justify-center 
                            group-hover:scale-110 transition-all duration-500 mb-6 animate-float">
                        <Upload className="w-6 h-6 theme-text-secondary group-hover:theme-text-primary transition-colors" />
                    </div>

                    <p className="text-base font-light tracking-wide theme-text-primary mb-2">
                        Drop your inspiration here
                    </p>
                    <p className="text-xs theme-text-tertiary tracking-wider">
                        PNG, JPG up to 5MB · Max 5 images
                    </p>
                </div>
            </div>

            {images.length > 0 && (
                <div className="grid grid-cols-5 gap-3">
                    {images.map((file, index) => (
                        <div
                            key={index}
                            className="relative aspect-square group animate-scale-in rounded-xl overflow-hidden"
                            style={{ animationDelay: `${index * 0.08}s` }}
                        >
                            <img
                                src={URL.createObjectURL(file)}
                                alt={`Upload ${index + 1}`}
                                className="w-full h-full object-cover
                                           transition-all duration-400 group-hover:scale-110"
                            />
                            <div className="absolute inset-0 bg-black/0 group-hover:bg-black/30 transition-all duration-300" />
                            <button
                                onClick={(e) => { e.stopPropagation(); removeImage(index) }}
                                className="absolute top-2 right-2 p-1.5 rounded-full
                                           bg-black/60 backdrop-blur-sm
                                           theme-text-secondary hover:text-white 
                                           opacity-0 group-hover:opacity-100 transition-all duration-300
                                           hover:scale-110 hover:bg-red-500/80"
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
