import { Loader2, ArrowRight } from 'lucide-react'

function SubmitButton({ disabled, onClick, loading }) {
    return (
        <button
            onClick={onClick}
            disabled={disabled || loading}
            className={`
        w-full py-4 rounded-xl font-light tracking-[0.2em] text-sm uppercase
        transition-all duration-500 relative overflow-hidden group
        ${disabled
                    ? 'bg-white/5 text-white/20 cursor-not-allowed border border-white/5'
                    : 'bg-white text-black hover:bg-white/90 shadow-[0_0_20px_rgba(255,255,255,0.1)] hover:shadow-[0_0_30px_rgba(255,255,255,0.2)]'
                }
      `}
        >
            <div className="flex items-center justify-center gap-3">
                {loading ? (
                    <>
                        <Loader2 className="w-4 h-4 animate-spin" />
                        <span>Processing</span>
                    </>
                ) : (
                    <>
                        <span>Analyze</span>
                        {!disabled && <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />}
                    </>
                )}
            </div>
        </button>
    )
}

export default SubmitButton
