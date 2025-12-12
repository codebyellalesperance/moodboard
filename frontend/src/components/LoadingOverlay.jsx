import { Loader2 } from 'lucide-react'

function LoadingOverlay() {
    return (
        <div className="fixed inset-0 bg-[var(--bg-primary)]/90 backdrop-blur-2xl z-50 
                    flex items-center justify-center animate-fade-in">
            <div className="text-center space-y-8">
                {/* Animated rings */}
                <div className="relative w-24 h-24 mx-auto">
                    <div className="absolute inset-0 rounded-full border-2 border-[var(--glass-border)] 
                                    animate-[spin_4s_linear_infinite]" />
                    <div className="absolute inset-3 rounded-full border-2 border-[var(--gradient-start)] 
                                    animate-[spin_3s_linear_infinite_reverse]" />
                    <div className="absolute inset-6 rounded-full border-2 border-[var(--gradient-mid)] 
                                    animate-[spin_2s_linear_infinite]" />
                    <div className="absolute inset-0 flex items-center justify-center">
                        <Loader2 className="w-6 h-6 theme-text-primary animate-spin" />
                    </div>
                </div>

                {/* Text */}
                <div className="space-y-2">
                    <p className="theme-text-primary font-medium text-lg tracking-wide">
                        Analyzing your style
                    </p>
                    <p className="theme-text-tertiary font-light text-sm tracking-wider animate-pulse">
                        Finding perfect matches...
                    </p>
                </div>
            </div>
        </div>
    )
}

export default LoadingOverlay
