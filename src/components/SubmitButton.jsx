function SubmitButton({ disabled, onClick, loading }) {
    return (
        <button
            onClick={onClick}
            disabled={disabled || loading}
            className={`w-full py-4 rounded-xl font-medium text-lg transition-all
        ${disabled || loading
                    ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                    : 'bg-gray-900 text-white hover:bg-gray-800 active:scale-[0.99]'
                }`}
        >
            {loading ? (
                <span className="flex items-center justify-center gap-2">
                    <span className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                    Analyzing your mood...
                </span>
            ) : (
                'Shop This Mood'
            )}
        </button>
    )
}

export default SubmitButton
