function ImageUploader() {
    return (
        <div className="w-full">
            <div
                className="border-2 border-dashed border-gray-300 rounded-xl p-12 text-center 
                   hover:border-gray-400 transition-colors cursor-pointer bg-white"
            >
                <div className="text-4xl mb-4">📷</div>
                <p className="text-gray-600 font-medium">
                    Drag & drop images or click to upload
                </p>
                <p className="text-gray-400 text-sm mt-2">
                    Up to 5 images • JPG, PNG, or WEBP
                </p>
            </div>
        </div>
    )
}

export default ImageUploader
