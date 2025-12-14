import { Loader2, ArrowRight, Sparkles, Zap } from 'lucide-react'

function SubmitButton({ disabled, onClick, loading }) {
    return (
        <button
            onClick={onClick}
            disabled={disabled || loading}
            className={`
                w-full py-6 rounded-2xl font-medium tracking-wide text-base
                transition-all duration-500 relative overflow-hidden group
                ${disabled
                    ? 'glass theme-text-tertiary cursor-not-allowed opacity-60'
                    : 'bg-gradient-to-r from-[var(--bg-secondary)] via-[var(--bg-primary)] to-[var(--bg-secondary)] text-[var(--accent)] border border-[var(--glass-border)] hover:border-[var(--glass-border-hover)] hover:shadow-2xl hover:scale-[1.02] active:scale-[0.98]'
                }
            `}
        >
            {/* Animated background shimmer */}
            {!disabled && !loading && (
                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-[var(--glass-border-hover)] to-transparent
                                translate-x-[-200%] group-hover:translate-x-[200%] transition-transform duration-1000 ease-out" />
            )}

            {/* Glow effect */}
            {!disabled && (
                <div className="absolute inset-0 bg-gradient-to-r from-[var(--glass-border)] to-[var(--glass-border-hover)] opacity-0 group-hover:opacity-30 blur-xl transition-opacity duration-500" />
            )}

            <div className="relative z-10 flex items-center justify-center gap-3">
                {loading ? (
                    <>
                        <Loader2 className="w-5 h-5 animate-spin" />
                        <span>Discovering your vibe...</span>
                    </>
                ) : (
                    <>
                        <Zap className="w-5 h-5" />
                        <span>Find My Style</span>
                        {!disabled && (
                            <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform duration-300" />
                        )}
                    </>
                )}
            </div>
        </button>
    )
}

export default SubmitButton
