import { TrendingUp, TrendingDown, Minus, Activity } from 'lucide-react'

function TrendGraph({ data, direction, width = 280, height = 60 }) {
    if (!data || data.length < 2) {
        return (
            <div className="flex items-center justify-center h-full text-[var(--color-text-secondary)] text-xs font-mono">
                NO_DATA_AVAILABLE
            </div>
        )
    }

    const min = Math.min(...data)
    const max = Math.max(...data)
    const range = max - min || 1

    const padding = { top: 8, right: 10, bottom: 20, left: 10 }
    const chartWidth = width - padding.left - padding.right
    const chartHeight = height - padding.top - padding.bottom

    // Generate smooth curve points
    const points = data.map((value, index) => {
        const x = padding.left + (index / (data.length - 1)) * chartWidth
        const y = padding.top + chartHeight - ((value - min) / range) * chartHeight
        return { x, y, value }
    })

    // Create polyline for tech look (sharper than bezier)
    const pathD = points.reduce((acc, point, i) => {
        if (i === 0) return `M ${point.x},${point.y}`
        return `${acc} L ${point.x},${point.y}`
    }, '')

    // Area path
    const areaD = `${pathD} L ${points[points.length - 1].x},${height - padding.bottom} L ${padding.left},${height - padding.bottom} Z`

    // Colors - Monochrome/Neon Tech
    const colors = {
        rising: { stroke: 'var(--color-text-primary)', gradient: ['var(--color-text-primary, rgba(255, 255, 255, 0.2))', 'rgba(255, 255, 255, 0)'] },
        falling: { stroke: 'var(--color-text-secondary)', gradient: ['var(--color-text-secondary, rgba(160, 160, 160, 0.2))', 'rgba(160, 160, 160, 0)'] },
        stable: { stroke: 'var(--color-text-secondary)', gradient: ['var(--color-text-secondary, rgba(170, 170, 170, 0.2))', 'rgba(170, 170, 170, 0)'] }
    }

    const { stroke, gradient } = colors[direction] || colors.stable
    const gradientId = `trend-gradient-${direction}`
    const labels = ['-3 MO', 'NOW']

    return (
        <svg width={width} height={height} className="w-full">
            <defs>
                <linearGradient id={gradientId} x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor={gradient[0]} />
                    <stop offset="100%" stopColor={gradient[1]} />
                </linearGradient>
            </defs>

            {/* Grid lines */}
            {[0, 0.5, 1].map((ratio, i) => (
                <line
                    key={i}
                    x1={padding.left}
                    y1={padding.top + chartHeight * ratio}
                    x2={width - padding.right}
                    y2={padding.top + chartHeight * ratio}
                    stroke="var(--border-color)"
                    strokeDasharray="2,2"
                    opacity={0.3}
                />
            ))}

            {/* Area fill */}
            <path d={areaD} fill={`url(#${gradientId})`} />

            {/* Line */}
            <path
                d={pathD}
                fill="none"
                stroke={stroke}
                strokeWidth={1.5}
                strokeLinecap="square"
                strokeLinejoin="round"
            />

            {/* End point dot */}
            <rect
                x={points[points.length - 1].x - 2}
                y={points[points.length - 1].y - 2}
                width={4}
                height={4}
                fill={stroke}
            />

            {/* X-axis labels */}
            <text x={padding.left} y={height - 5} className="text-[8px] font-mono fill-[var(--text-secondary)]">
                {labels[0]}
            </text>
            <text x={width - padding.right} y={height - 5} textAnchor="end" className="text-[8px] font-mono fill-[var(--content-secondary)]">
                {labels[1]}
            </text>
        </svg>
    )
}

function TrendCard({ trend }) {
    if (!trend || trend.direction === 'unknown') {
        return null
    }

    const config = {
        rising: {
            icon: TrendingUp,
            label: 'Uptrend',
            description: 'Gaining momentum',
            colorClass: 'text-[var(--color-text-primary)]'
        },
        falling: {
            icon: TrendingDown,
            label: 'Downtrend',
            description: 'Declining interest',
            colorClass: 'text-[var(--color-text-secondary)]'
        },
        stable: {
            icon: Minus,
            label: 'Stable',
            description: 'Consistent volume',
            colorClass: 'text-[var(--color-text-secondary)]'
        }
    }

    const { icon: Icon, label, colorClass } = config[trend.direction] || config.stable

    return (
        <div className="border border-[var(--border-color)] p-6 animate-scale-in bg-[var(--bg-secondary)]">
            <div className="flex items-center gap-6">
                {/* Left: Icon + Label */}
                <div className="shrink-0 space-y-2">
                    <div className="flex items-center gap-2">
                        <p className="font-mono text-[10px] uppercase tracking-widest text-[var(--color-text-secondary)]">Market_Signal</p>
                        {trend.searched_term && trend.searched_term !== trend.keyword && (
                            <span className="font-mono text-[9px] text-[var(--color-text-tertiary)]">
                                ({trend.searched_term})
                            </span>
                        )}
                    </div>
                    <div className="flex items-center gap-2">
                        <Icon className={`w-4 h-4 ${colorClass}`} />
                        <span className={`font-mono text-sm uppercase ${colorClass}`}>{label}</span>
                    </div>
                    {trend.change && (
                        <span className="block font-sans text-xs text-[var(--color-text-primary)]">{trend.change}</span>
                    )}
                </div>

                {/* Center: Graph */}
                <div className="flex-1 min-w-0 border-l border-[var(--border-color)] pl-6">
                    <TrendGraph
                        data={trend.sparkline}
                        direction={trend.direction}
                        width={200}
                        height={50}
                    />
                </div>

                {/* Right: Stats */}
                {trend.current !== null && (
                    <div className="shrink-0 text-right border-l border-[var(--border-color)] pl-6 space-y-2">
                        <div>
                            <p className="font-mono text-[10px] uppercase tracking-widest text-[var(--color-text-secondary)]">Volume</p>
                            <p className="font-serif text-xl italic text-[var(--color-text-primary)]">{trend.current}</p>
                        </div>
                    </div>
                )}
            </div>
        </div>
    )
}

export default TrendCard
