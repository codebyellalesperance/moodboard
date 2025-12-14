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
        <div className="space-y-4">
            <div className="flex items-center gap-2 mb-2 opacity-70">
                <ImageIcon className="w-3 h-3 text-[var(--color-text-secondary)]" />
                <span className="font-mono text-xs tracking-widest uppercase text-[var(--color-text-secondary)]">
                    Visual_Reference_Upload
                </span>
            </div>

            <div
                onClick={() => fileInputRef.current?.click()}
                onDragOver={(e) => e.preventDefault()}
                onDrop={handleDrop}
                className="group relative cursor-pointer min-h-[200px] flex flex-col items-center justify-center
                   border border-dashed border-[var(--border-color)] hover:border-[var(--color-text-primary)]
                   bg-[var(--bg-secondary)] hover:bg-[var(--bg-primary)]
                   transition-all duration-300"
            >
                <input
                    type="file"
                    ref={fileInputRef}
                    onChange={handleFileSelect}
                    className="hidden"
                    accept="image/*"
                    multiple
                />

                {/* Crosshairs */}
                <div className="absolute top-0 left-0 w-3 h-3 border-t border-l border-[var(--color-text-secondary)]" />
                <div className="absolute top-0 right-0 w-3 h-3 border-t border-r border-[var(--color-text-secondary)]" />
                <div className="absolute bottom-0 left-0 w-3 h-3 border-b border-l border-[var(--color-text-secondary)]" />
                <div className="absolute bottom-0 right-0 w-3 h-3 border-b border-r border-[var(--color-text-secondary)]" />

                <div className="flex flex-col items-center gap-4 group-hover:scale-105 transition-transform">
                    <div className="p-3 border border-[var(--border-color)] rounded-full">
                        <Upload className="w-5 h-5 text-[var(--color-text-primary)]" />
                    </div>
                    <div className="text-center">
                        <p className="font-serif italic text-lg text-[var(--color-text-primary)]">Drop files here</p>
                        <p className="font-mono text-[10px] uppercase tracking-widest text-[var(--color-text-secondary)] mt-1">
                            or click to browse
                        </p>
                    </div>
                </div>
            </div>

            {images.length > 0 && (
                <div className="grid grid-cols-5 gap-2">
                    {images.map((file, index) => (
                        <div
                            key={index}
                            className="relative aspect-[3/4] group border border-[var(--border-color)]"
                        >
                            <img
                                src={URL.createObjectURL(file)}
                                alt={`Upload ${index + 1}`}
                                className="w-full h-full object-cover grayscale group-hover:grayscale-0 transition-all duration-500"
                            />
                            <button
                                onClick={(e) => { e.stopPropagation(); removeImage(index) }}
                                className="absolute top-0 right-0 p-1 bg-black text-white hover:bg-white hover:text-black transition-colors"
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
