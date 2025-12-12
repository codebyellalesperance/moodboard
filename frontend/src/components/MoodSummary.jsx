import { Palette, Shirt, Sparkles } from 'lucide-react'

function MoodSummary({ mood }) {
    if (!mood) return null

    return (
        <div className="space-y-10 animate-slide-up">
            {/* Header with badge */}
            <div className="text-center space-y-5">
                <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass mb-4">
                    <Sparkles className="w-4 h-4 theme-text-secondary" />
                    <span className="text-xs font-medium tracking-wider theme-text-secondary uppercase">
                        Your Vibe
                    </span>
                </div>

                <h2 className="text-5xl font-extralight tracking-tight theme-text-primary">
                    {mood.name}
                </h2>
                <p className="theme-text-secondary font-light text-lg tracking-wide max-w-md mx-auto">
                    {mood.mood}
                </p>
            </div>

            <div className="grid md:grid-cols-2 gap-6">
                {/* Palette */}
                <div className="glass-card rounded-3xl p-8 space-y-6 animate-scale-in opacity-0"
                    style={{ animationDelay: '0.2s', animationFillMode: 'forwards' }}>
                    <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-xl glass flex items-center justify-center">
                            <Palette className="w-5 h-5 theme-text-secondary" />
                        </div>
                        <h3 className="text-sm font-medium tracking-wider theme-text-primary uppercase">
                            Color Palette
                        </h3>
                    </div>
                    <div className="flex gap-4 justify-start">
                        {mood.color_palette.map((color, index) => (
                            <div
                                key={index}
                                className="group relative animate-scale-in opacity-0"
                                style={{ animationDelay: `${0.3 + index * 0.1}s`, animationFillMode: 'forwards' }}
                            >
                                <div
                                    className="w-14 h-14 rounded-2xl border-2 border-white/10
                                               shadow-lg transition-all duration-300 
                                               group-hover:scale-110 group-hover:shadow-xl 
                                               group-hover:rotate-3 cursor-pointer"
                                    style={{ backgroundColor: color.hex }}
                                />
                                <span className="absolute -bottom-7 left-1/2 -translate-x-1/2 text-[10px] 
                                 theme-text-secondary opacity-0 group-hover:opacity-100 whitespace-nowrap 
                                 transition-all duration-300 tracking-wide capitalize font-medium">
                                    {color.name}
                                </span>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Key Pieces */}
                <div className="glass-card rounded-3xl p-8 space-y-6 animate-scale-in opacity-0"
                    style={{ animationDelay: '0.35s', animationFillMode: 'forwards' }}>
                    <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-xl glass flex items-center justify-center">
                            <Shirt className="w-5 h-5 theme-text-secondary" />
                        </div>
                        <h3 className="text-sm font-medium tracking-wider theme-text-primary uppercase">
                            Key Pieces
                        </h3>
                    </div>
                    <div className="flex flex-wrap gap-2">
                        {mood.key_pieces.map((piece, index) => (
                            <span
                                key={index}
                                className="px-4 py-2.5 rounded-xl glass
                             text-xs theme-text-primary font-medium tracking-wide
                             hover:bg-[var(--glass-bg-hover)] transition-all duration-300
                             hover:scale-105 cursor-default animate-scale-in opacity-0"
                                style={{ animationDelay: `${0.45 + index * 0.05}s`, animationFillMode: 'forwards' }}
                            >
                                {piece}
                            </span>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    )
}

export default MoodSummary
