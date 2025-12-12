function LoadingOverlay() {
    return (
        <div className="fixed inset-0 bg-white/90 backdrop-blur-sm z-50 
                    flex items-center justify-center">
            <div className="text-center">
                <div className="w-12 h-12 border-3 border-gray-200 border-t-gray-900 
                        rounded-full animate-spin mx-auto" />
                <p className="mt-4 text-gray-600 font-medium">Analyzing your mood...</p>
                <p className="mt-2 text-gray-400 text-sm">This takes about 10 seconds</p>
            </div>
        </div>
    )
}

export default LoadingOverlay
