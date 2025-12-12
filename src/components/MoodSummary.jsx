function MoodSummary({ mood }) {
    if (!mood) return null

    return (
        <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-700">
            {/* Header */}
            <div className="text-center space-y-2">
                <h2 className="text-3xl font-light tracking-tight text-white">
                    {mood.name}
                </h2>
                <p className="text-white/60 font-light text-sm tracking-wide">
                    {mood.mood}
                </p>
            </div>

            {/* Palette */}
            <div className="glass rounded-2xl p-6 space-y-4">
                <h3 className="text-xs font-medium tracking-[0.2em] text-white/40 uppercase">
                    Palette
                </h3>
                <div className="flex gap-4">
                    {mood.color_palette.map((color, index) => (
                        <div key={index} className="group relative">
                            <div
                                className="w-12 h-12 rounded-full border border-white/10 shadow-lg transition-transform group-hover:scale-110"
                                style={{ backgroundColor: color.hex }}
                            />
                            <span className="absolute -bottom-6 left-1/2 -translate-x-1/2 text-[10px] 
                             text-white/60 opacity-0 group-hover:opacity-100 whitespace-nowrap 
                             transition-opacity tracking-wide uppercase">
                                {color.name}
                            </span>
                        </div>
                    ))}
                </div>
            </div>

            {/* Key Pieces */}
            <div className="glass rounded-2xl p-6 space-y-4">
                <h3 className="text-xs font-medium tracking-[0.2em] text-white/40 uppercase">
                    Essentials
                </h3>
                <div className="flex flex-wrap gap-2">
                    {mood.key_pieces.map((piece, index) => (
                        <span
                            key={index}
                            className="px-3 py-1.5 rounded-full border border-white/10 bg-white/5 
                         text-xs text-white/80 font-light tracking-wide"
                        >
                            {piece}
                        </span>
                    ))}
                </div>
            </div>
        </div>
    )
}

export default MoodSummary
