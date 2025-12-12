import { Loader2, ArrowRight, Sparkles } from 'lucide-react'

function SubmitButton({ disabled, onClick, loading }) {
    return (
        <button
            onClick={onClick}
            disabled={disabled || loading}
            className={`
                w-full py-5 rounded-2xl font-medium tracking-[0.15em] text-sm uppercase
                transition-all duration-500 relative overflow-hidden group
                ${disabled
                    ? 'glass theme-text-tertiary cursor-not-allowed'
                    : 'bg-gradient-to-r from-[var(--accent)] to-[var(--accent-muted)] text-[var(--bg-primary)] hover:shadow-2xl animate-pulse-glow'
                }
            `}
        >
            {/* Shimmer effect */}
            {!disabled && !loading && (
                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent 
                                translate-x-[-200%] group-hover:translate-x-[200%] transition-transform duration-1000" />
            )}

            <div className="relative z-10 flex items-center justify-center gap-3">
                {loading ? (
                    <>
                        <Loader2 className="w-5 h-5 animate-spin" />
                        <span>Analyzing your vibe...</span>
                    </>
                ) : (
                    <>
                        <Sparkles className="w-4 h-4" />
                        <span>Analyze My Style</span>
                        {!disabled && (
                            <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform duration-300" />
                        )}
                    </>
                )}
            </div>
        </button>
    )
}

export default SubmitButton
