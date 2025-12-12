function MoodSummary({ mood }) {
    if (!mood) return null

    return (
        <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
            {/* Mood Name */}
            <h2 className="text-2xl font-semibold text-gray-900">
                {mood.name}
            </h2>

            {/* Mood Description */}
            <p className="mt-2 text-gray-500">
                {mood.mood}
            </p>

            {/* Color Palette */}
            <div className="mt-4">
                <p className="text-sm text-gray-400 mb-2">Color Palette</p>
                <div className="flex gap-2">
                    {mood.color_palette.map((color, index) => (
                        <div key={index} className="group relative">
                            <div
                                className="w-10 h-10 rounded-full border border-gray-200"
                                style={{ backgroundColor: color.hex }}
                            />
                            <span className="absolute -bottom-6 left-1/2 -translate-x-1/2 text-xs 
                             text-gray-500 opacity-0 group-hover:opacity-100 transition-opacity
                             whitespace-nowrap">
                                {color.name}
                            </span>
                        </div>
                    ))}
                </div>
            </div>

            {/* Key Pieces */}
            <div className="mt-8">
                <p className="text-sm text-gray-400 mb-2">Key Pieces</p>
                <div className="flex flex-wrap gap-2">
                    {mood.key_pieces.map((piece, index) => (
                        <span
                            key={index}
                            className="px-3 py-1 bg-gray-100 rounded-full text-sm text-gray-700"
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
