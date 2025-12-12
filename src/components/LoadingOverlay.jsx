import { Loader2 } from 'lucide-react'

function LoadingOverlay() {
    return (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-xl z-50 
                    flex items-center justify-center">
            <div className="text-center space-y-4">
                <div className="relative">
                    <div className="w-16 h-16 rounded-full border border-white/10 animate-[spin_3s_linear_infinite]" />
                    <div className="w-12 h-12 rounded-full border border-white/20 animate-[spin_2s_linear_infinite_reverse] absolute top-2 left-2" />
                    <Loader2 className="w-6 h-6 text-white absolute top-5 left-5 animate-spin" />
                </div>
                <p className="text-white/60 font-light text-sm tracking-[0.2em] uppercase animate-pulse">
                    Analyzing
                </p>
            </div>
        </div>
    )
}

export default LoadingOverlay
