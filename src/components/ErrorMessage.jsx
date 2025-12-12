import { AlertCircle, RefreshCw } from 'lucide-react'

function ErrorMessage({ message, onRetry }) {
    return (
        <div className="p-6 glass rounded-xl text-center space-y-3 border-red-500/20 bg-red-500/5">
            <div className="flex justify-center">
                <AlertCircle className="w-6 h-6 text-red-400" />
            </div>
            <p className="text-red-200/80 text-sm font-light">{message}</p>
            {onRetry && (
                <button
                    onClick={onRetry}
                    className="inline-flex items-center gap-2 px-4 py-2 rounded-lg 
                     bg-red-500/10 hover:bg-red-500/20 text-red-300 text-xs 
                     tracking-wide uppercase transition-colors"
                >
                    <RefreshCw className="w-3 h-3" />
                    Retry
                </button>
            )}
        </div>
    )
}

export default ErrorMessage
