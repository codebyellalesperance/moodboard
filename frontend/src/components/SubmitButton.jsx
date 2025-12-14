import { Component, Loader2, ArrowRight, Sparkles, Zap } from 'lucide-react'

function SubmitButton({ disabled, onClick, loading }) {
    return (
        <button
            onClick={onClick}
            disabled={disabled || loading}
            className={`
                w-full py-4 text-sm font-mono tracking-[0.2em] uppercase
                transition-all duration-300 relative group border
                ${disabled
                    ? 'border-[var(--border-color)] text-[var(--color-text-secondary)] cursor-not-allowed opacity-50'
                    : 'bg-[var(--color-text-primary)] text-[var(--color-bg-primary)] border-[var(--color-text-primary)] hover:bg-transparent hover:text-[var(--color-text-primary)]'
                }
            `}
        >
            <div className="relative z-10 flex items-center justify-center gap-3">
                {loading ? (
                    <>
                        <Loader2 className="w-4 h-4 animate-spin" />
                        <span>Processing_Data...</span>
                    </>
                ) : (
                    <>
                        <span>Initialize_Search</span>
                        {!disabled && (
                            <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                        )}
                    </>
                )}
            </div>

            {/* Tech Decoration */}
            {!disabled && (
                <>
                    <div className="absolute top-0 right-0 w-2 h-2 bg-[var(--color-bg-primary)] group-hover:bg-[var(--color-text-primary)] transition-colors" />
                    <div className="absolute bottom-0 left-0 w-2 h-2 bg-[var(--color-bg-primary)] group-hover:bg-[var(--color-text-primary)] transition-colors" />
                </>
            )}
        </button>
    )
}

export default SubmitButton
