import { Palette, Shirt, Sparkles } from 'lucide-react'
import TrendCard from './TrendCard'

function MoodSummary({ mood, trend }) {
    if (!mood) return null

    return (
        <div className="space-y-16 animate-slide-up">
            {/* Header / Vibe Title */}
            <div className="border-b border-[var(--border-color)] pb-12">
                <div className="flex items-center gap-2 mb-4">
                    <span className="font-mono text-xs uppercase tracking-[0.3em] text-[var(--color-text-secondary)]">
                        Analysis_Result
                    </span>
                    <div className="h-px w-12 bg-[var(--color-text-secondary)]" />
                </div>

                <h2 className="font-serif text-7xl md:text-8xl leading-none tracking-tight mb-8 text-[var(--color-text-primary)]">
                    {mood.name}
                </h2>

                <p className="font-sans text-xl font-light leading-relaxed max-w-2xl text-[var(--color-text-secondary)] border-l border-[var(--color-text-primary)] pl-6">
                    {mood.mood}
                </p>
            </div>

            {/* Trend Analysis */}
            {trend && trend.direction !== 'unknown' && (
                <div className="animate-scale-in opacity-0" style={{ animationDelay: '0.15s', animationFillMode: 'forwards' }}>
                    <TrendCard trend={trend} />
                </div>
            )}

            {/* Details Grid */}
            <div className="grid grid-cols-1 md:grid-cols-12 gap-12">
                {/* Palette */}
                <div className="md:col-span-12 lg:col-span-7 space-y-6">
                    <h3 className="font-serif text-3xl italic text-[var(--color-text-primary)]">Color Theory</h3>

                    <div className="grid grid-cols-5 gap-0 border border-[var(--border-color)]">
                        {mood.color_palette.map((color, index) => (
                            <div key={index} className="aspect-square group relative border-r border-[var(--border-color)] last:border-r-0">
                                <div className="w-full h-full" style={{ backgroundColor: color.hex }} />
                                <div className="absolute inset-0 flex flex-col items-center justify-center bg-black/80 opacity-0 group-hover:opacity-100 transition-opacity p-2 text-center">
                                    <span className="font-mono text-[10px] uppercase text-white mb-1">{color.hex}</span>
                                    <span className="font-serif text-xs italic text-[var(--color-text-secondary)]">{color.name}</span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Key Pieces */}
                <div className="md:col-span-12 lg:col-span-5 space-y-6">
                    <h3 className="font-serif text-3xl italic text-[var(--color-text-primary)]">Key Elements</h3>

                    <ul className="space-y-4 font-mono text-sm uppercase tracking-wider">
                        {mood.key_pieces.map((piece, index) => (
                            <li key={index} className="flex items-center gap-4 border-b border-[var(--border-color)] pb-2 group">
                                <span className="text-[var(--color-text-secondary)] group-hover:text-[var(--color-accent)] transition-colors">0{index + 1}</span>
                                <span className="text-[var(--color-text-primary)]">{piece}</span>
                            </li>
                        ))}
                    </ul>
                </div>
            </div>
        </div>
    )
}

export default MoodSummary
