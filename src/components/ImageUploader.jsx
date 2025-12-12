import { useState, useRef } from 'react'

function ImageUploader({ images, setImages }) {
    const fileInputRef = useRef(null)
    const [isDragging, setIsDragging] = useState(false)

    const handleFiles = (files) => {
        const validFiles = Array.from(files).filter(file => {
            // Check if image
            if (!file.type.startsWith('image/')) {
                alert(`${file.name} is not an image`)
                return false
            }
            // Check size (5MB max)
            if (file.size > 5 * 1024 * 1024) {
                alert(`${file.name} is too large (max 5MB)`)
                return false
            }
            return true
        })

        // Check total count
        const totalImages = images.length + validFiles.length
        if (totalImages > 5) {
            alert('Maximum 5 images allowed')
            const allowedCount = 5 - images.length
            validFiles.splice(allowedCount)
        }

        if (validFiles.length > 0) {
            setImages([...images, ...validFiles])
        }
    }

    const handleClick = () => {
        fileInputRef.current?.click()
    }

    const handleFileChange = (e) => {
        if (e.target.files) {
            handleFiles(e.target.files)
        }
        // Reset input so same file can be selected again
        e.target.value = ''
    }

    const handleDragOver = (e) => {
        e.preventDefault()
        setIsDragging(true)
    }

    const handleDragLeave = (e) => {
        e.preventDefault()
        setIsDragging(false)
    }

    const handleDrop = (e) => {
        e.preventDefault()
        setIsDragging(false)
        if (e.dataTransfer.files) {
            handleFiles(e.dataTransfer.files)
        }
    }

    const removeImage = (index) => {
        setImages(images.filter((_, i) => i !== index))
    }

    return (
        <div className="w-full">
            {/* Hidden file input */}
            <input
                type="file"
                ref={fileInputRef}
                onChange={handleFileChange}
                accept="image/jpeg,image/png,image/webp"
                multiple
                className="hidden"
            />

            {/* Upload zone */}
            <div
                onClick={handleClick}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                className={`border-2 border-dashed rounded-xl p-12 text-center transition-colors cursor-pointer bg-white
          ${isDragging ? 'border-gray-900 bg-gray-50' : 'border-gray-300 hover:border-gray-400'}`}
            >
                <div className="text-4xl mb-4">📷</div>
                <p className="text-gray-600 font-medium">
                    Drag & drop images or click to upload
                </p>
                <p className="text-gray-400 text-sm mt-2">
                    {images.length}/5 images • JPG, PNG, or WEBP
                </p>
            </div>

            {/* Image previews */}
            {images.length > 0 && (
                <div className="mt-4 flex flex-wrap gap-3">
                    {images.map((file, index) => (
                        <div key={index} className="relative group">
                            <img
                                src={URL.createObjectURL(file)}
                                alt={`Upload ${index + 1}`}
                                className="w-20 h-20 object-cover rounded-lg"
                            />
                            <button
                                onClick={(e) => {
                                    e.stopPropagation()
                                    removeImage(index)
                                }}
                                className="absolute -top-2 -right-2 w-6 h-6 bg-gray-900 text-white rounded-full 
                           text-sm flex items-center justify-center opacity-0 group-hover:opacity-100 
                           transition-opacity"
                            >
                                ×
                            </button>
                        </div>
                    ))}
                </div>
            )}
        </div>
    )
}

export default ImageUploader
