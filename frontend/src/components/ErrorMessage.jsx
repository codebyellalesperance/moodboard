import { AlertCircle, RefreshCw } from 'lucide-react'

function ErrorMessage({ message, onRetry }) {
    return (
        <div className="glass rounded-2xl p-6 flex items-center gap-4 animate-scale-in
                        border-red-500/20">
            <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0" />
            <p className="text-sm theme-text-secondary flex-1">{message}</p>
            {onRetry && (
                <button
                    onClick={onRetry}
                    className="p-2.5 rounded-full glass glass-hover transition-all duration-300
                               hover:scale-110 group"
                >
                    <RefreshCw className="w-4 h-4 theme-text-secondary group-hover:theme-text-primary 
                                          transition-colors" />
                </button>
            )}
        </div>
    )
}

export default ErrorMessage
