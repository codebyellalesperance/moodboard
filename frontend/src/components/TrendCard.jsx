import { TrendingUp, TrendingDown, Minus, Activity } from 'lucide-react'

function TrendGraph({ data, direction, width = 280, height = 60 }) {
    if (!data || data.length < 2) {
        return (
            <div className="flex items-center justify-center h-full theme-text-tertiary text-sm">
                No trend data available
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

    // Create smooth bezier curve path
    const pathD = points.reduce((acc, point, i) => {
        if (i === 0) return `M ${point.x},${point.y}`
        const prev = points[i - 1]
        const cpX = (prev.x + point.x) / 2
        return `${acc} C ${cpX},${prev.y} ${cpX},${point.y} ${point.x},${point.y}`
    }, '')

    // Area path for gradient fill
    const areaD = `${pathD} L ${points[points.length - 1].x},${height - padding.bottom} L ${padding.left},${height - padding.bottom} Z`

    // Colors based on direction
    const colors = {
        rising: { stroke: '#34d399', gradient: ['rgba(52, 211, 153, 0.3)', 'rgba(52, 211, 153, 0)'] },
        falling: { stroke: '#94a3b8', gradient: ['rgba(148, 163, 184, 0.2)', 'rgba(148, 163, 184, 0)'] },
        stable: { stroke: '#fbbf24', gradient: ['rgba(251, 191, 36, 0.25)', 'rgba(251, 191, 36, 0)'] }
    }

    const { stroke, gradient } = colors[direction] || colors.stable
    const gradientId = `trend-gradient-${direction}`

    // X-axis labels (3 months ago, now)
    const labels = ['3 months ago', 'Now']

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
                    stroke="var(--glass-border)"
                    strokeDasharray="4,4"
                    opacity={0.5}
                />
            ))}

            {/* Area fill */}
            <path d={areaD} fill={`url(#${gradientId})`} />

            {/* Line */}
            <path
                d={pathD}
                fill="none"
                stroke={stroke}
                strokeWidth={2.5}
                strokeLinecap="round"
                strokeLinejoin="round"
            />

            {/* End point dot */}
            <circle
                cx={points[points.length - 1].x}
                cy={points[points.length - 1].y}
                r={4}
                fill={stroke}
            />
            <circle
                cx={points[points.length - 1].x}
                cy={points[points.length - 1].y}
                r={8}
                fill={stroke}
                opacity={0.2}
            />

            {/* X-axis labels */}
            <text
                x={padding.left}
                y={height - 5}
                className="text-[10px] fill-[var(--text-tertiary)]"
            >
                {labels[0]}
            </text>
            <text
                x={width - padding.right}
                y={height - 5}
                textAnchor="end"
                className="text-[10px] fill-[var(--text-tertiary)]"
            >
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
            label: 'Rising',
            description: 'This aesthetic is gaining popularity',
            colorClass: 'text-emerald-400',
            bgClass: 'bg-emerald-500/10'
        },
        falling: {
            icon: TrendingDown,
            label: 'Cooling Off',
            description: 'Interest has decreased recently',
            colorClass: 'text-slate-400',
            bgClass: 'bg-slate-500/10'
        },
        stable: {
            icon: Minus,
            label: 'Steady',
            description: 'Consistent interest over time',
            colorClass: 'text-amber-400',
            bgClass: 'bg-amber-500/10'
        }
    }

    const { icon: Icon, label, description, colorClass, bgClass } = config[trend.direction] || config.stable

    return (
        <div className="glass-card rounded-2xl p-4 animate-scale-in">
            <div className="flex items-center gap-4">
                {/* Left: Icon + Label */}
                <div className="flex items-center gap-3 shrink-0">
                    <div className={`w-8 h-8 rounded-lg ${bgClass} flex items-center justify-center`}>
                        <Activity className={`w-4 h-4 ${colorClass}`} />
                    </div>
                    <div>
                        <p className="text-xs theme-text-tertiary">Trend</p>
                        <div className="flex items-center gap-1.5">
                            <Icon className={`w-3.5 h-3.5 ${colorClass}`} />
                            <span className={`text-sm font-medium ${colorClass}`}>{label}</span>
                            {trend.change && (
                                <span className={`text-sm font-bold ${colorClass}`}>{trend.change}</span>
                            )}
                        </div>
                    </div>
                </div>

                {/* Center: Graph */}
                <div className="flex-1 min-w-0">
                    <TrendGraph
                        data={trend.sparkline}
                        direction={trend.direction}
                        width={200}
                        height={50}
                    />
                </div>

                {/* Right: Stats */}
                {trend.current !== null && (
                    <div className="flex items-center gap-4 shrink-0 text-right">
                        <div>
                            <p className="text-[10px] theme-text-tertiary uppercase">Now</p>
                            <p className="text-sm font-medium theme-text-primary">{trend.current}</p>
                        </div>
                        {trend.peak && trend.peak !== 'now' && (
                            <div>
                                <p className="text-[10px] theme-text-tertiary uppercase">Peak</p>
                                <p className="text-sm font-medium theme-text-primary capitalize">{trend.peak}</p>
                            </div>
                        )}
                    </div>
                )}
            </div>
        </div>
    )
}

export default TrendCard
