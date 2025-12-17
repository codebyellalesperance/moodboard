import { Palette, Shirt, Sparkles, Calendar, Sun, User, Tag, TrendingUp } from 'lucide-react'
import TrendCard from './TrendCard'

function MoodSummary({ mood, trend }) {
    if (!mood) return null

    // Get confidence level label
    const getConfidenceLabel = (score) => {
        if (score >= 0.9) return 'Very High'
        if (score >= 0.75) return 'High'
        if (score >= 0.6) return 'Moderate'
        return 'Low'
    }

    // Season emoji helper
    const seasonEmoji = {
        spring: '🌸',
        summer: '☀️',
        fall: '🍂',
        winter: '❄️'
    }

    return (
        <div className="space-y-6 sm:space-y-8 animate-slide-up">
            {/* Header / Vibe Title */}
            <div className="border-b border-[var(--border-color)] pb-4 sm:pb-6">
                <div className="flex items-center gap-2 mb-2">
                    <span className="font-mono text-[10px] sm:text-xs uppercase tracking-[0.2em] text-[var(--color-text-secondary)]">
                        Analysis_Result
                    </span>
                    <div className="h-px w-8 bg-[var(--color-text-secondary)]" />
                    {mood.confidence && (
                        <span className="ml-auto font-mono text-[10px] uppercase tracking-wider text-[var(--color-text-tertiary)]">
                            {getConfidenceLabel(mood.confidence.overall)} confidence
                        </span>
                    )}
                </div>

                <h2 className="font-serif text-3xl sm:text-4xl md:text-5xl leading-none tracking-tight mb-3 sm:mb-4 text-[var(--color-text-primary)]">
                    {mood.name}
                </h2>

                <p className="font-sans text-sm sm:text-base font-light leading-relaxed max-w-2xl text-[var(--color-text-secondary)] border-l border-[var(--color-text-primary)] pl-4">
                    {mood.mood}
                </p>

                {/* Style Archetype + Gender Tags */}
                <div className="flex flex-wrap items-center gap-2 mt-4">
                    {mood.gender && (
                        <span className="inline-flex items-center gap-1.5 px-2.5 py-1 bg-[var(--color-bg-secondary)] border border-[var(--border-color)] font-mono text-[10px] uppercase tracking-wider text-[var(--color-text-secondary)]">
                            <User size={10} />
                            {mood.gender}
                        </span>
                    )}
                    {mood.style_archetype?.primary && (
                        <span className="inline-flex items-center gap-1.5 px-2.5 py-1 bg-[var(--color-bg-secondary)] border border-[var(--color-accent)] font-mono text-[10px] uppercase tracking-wider text-[var(--color-accent)]">
                            <Sparkles size={10} />
                            {mood.style_archetype.primary}
                        </span>
                    )}
                    {mood.style_archetype?.secondary && (
                        <span className="inline-flex items-center gap-1.5 px-2.5 py-1 bg-[var(--color-bg-secondary)] border border-[var(--border-color)] font-mono text-[10px] uppercase tracking-wider text-[var(--color-text-secondary)]">
                            + {mood.style_archetype.secondary}
                        </span>
                    )}
                </div>

                {/* Style Description */}
                {mood.style_archetype?.description && (
                    <p className="mt-3 font-sans text-xs text-[var(--color-text-tertiary)] italic max-w-xl">
                        {mood.style_archetype.description}
                    </p>
                )}
            </div>

            {/* Trend Analysis */}
            {trend && trend.direction !== 'unknown' && (
                <div className="animate-scale-in opacity-0" style={{ animationDelay: '0.15s', animationFillMode: 'forwards' }}>
                    <TrendCard trend={trend} />
                </div>
            )}

            {/* Occasions & Season Row */}
            {(mood.occasions?.length > 0 || mood.season) && (
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6">
                    {/* Occasions */}
                    {mood.occasions?.length > 0 && (
                        <div className="space-y-2">
                            <div className="flex items-center gap-2">
                                <Calendar size={14} className="text-[var(--color-text-secondary)]" />
                                <span className="font-mono text-[10px] uppercase tracking-[0.15em] text-[var(--color-text-secondary)]">
                                    Perfect For
                                </span>
                            </div>
                            <div className="flex flex-wrap gap-2">
                                {mood.occasions.map((occasion, index) => (
                                    <span
                                        key={index}
                                        className="px-3 py-1.5 bg-[var(--color-bg-secondary)] border border-[var(--border-color)] font-mono text-[10px] uppercase tracking-wider text-[var(--color-text-primary)] hover:border-[var(--color-accent)] transition-colors"
                                    >
                                        {occasion}
                                    </span>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* Season */}
                    {mood.season && (
                        <div className="space-y-2">
                            <div className="flex items-center gap-2">
                                <Sun size={14} className="text-[var(--color-text-secondary)]" />
                                <span className="font-mono text-[10px] uppercase tracking-[0.15em] text-[var(--color-text-secondary)]">
                                    Seasonality
                                </span>
                            </div>
                            <div className="space-y-2">
                                <div className="flex flex-wrap gap-2">
                                    {mood.season.best_for?.map((season, index) => (
                                        <span
                                            key={index}
                                            className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-[var(--color-bg-secondary)] border border-[var(--border-color)] font-mono text-[10px] uppercase tracking-wider text-[var(--color-text-primary)]"
                                        >
                                            {seasonEmoji[season] || ''} {season}
                                        </span>
                                    ))}
                                    {mood.season.adaptable && (
                                        <span className="px-3 py-1.5 border border-dashed border-[var(--color-text-tertiary)] font-mono text-[10px] uppercase tracking-wider text-[var(--color-text-tertiary)]">
                                            Year-round adaptable
                                        </span>
                                    )}
                                </div>
                                {mood.season.current_season_tips && (
                                    <p className="font-sans text-xs text-[var(--color-text-tertiary)] italic pl-1">
                                        💡 {mood.season.current_season_tips}
                                    </p>
                                )}
                            </div>
                        </div>
                    )}
                </div>
            )}

            {/* Details Grid */}
            <div className="space-y-6">
                {/* Palette */}
                <div className="space-y-3">
                    <h3 className="font-serif text-xl sm:text-2xl italic text-[var(--color-text-primary)]">Color Theory</h3>

                    <div className="grid grid-cols-5 gap-0 border border-[var(--border-color)]">
                        {mood.color_palette.map((color, index) => (
                            <div key={index} className="aspect-square group relative border-r border-[var(--border-color)] last:border-r-0">
                                <div className="w-full h-full" style={{ backgroundColor: color.hex }} />
                                <div className="absolute inset-0 flex flex-col items-center justify-center bg-black/80 opacity-0 group-hover:opacity-100 transition-opacity p-1 text-center">
                                    <span className="font-mono text-[8px] uppercase text-white">{color.hex}</span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Key Pieces */}
                <div className="space-y-3">
                    <h3 className="font-serif text-xl sm:text-2xl italic text-[var(--color-text-primary)]">Key Elements</h3>

                    <ul className="space-y-2 font-mono text-xs uppercase tracking-wider">
                        {mood.key_pieces.map((piece, index) => (
                            <li key={index} className="flex items-center gap-3 border-b border-[var(--border-color)] pb-1.5 group">
                                <span className="text-[var(--color-text-secondary)] group-hover:text-[var(--color-accent)] transition-colors text-[10px]">0{index + 1}</span>
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
