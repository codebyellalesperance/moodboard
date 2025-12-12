function ErrorMessage({ message, onRetry }) {
    return (
        <div className="p-6 bg-red-50 border border-red-200 rounded-xl text-center">
            <p className="text-red-600">{message}</p>
            {onRetry && (
                <button
                    onClick={onRetry}
                    className="mt-3 px-4 py-2 bg-red-100 hover:bg-red-200 
                     rounded-lg text-red-700 text-sm transition-colors"
                >
                    Try Again
                </button>
            )}
        </div>
    )
}

export default ErrorMessage
