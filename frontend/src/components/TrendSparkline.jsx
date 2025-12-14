function TrendSparkline({ data, direction, width = 60, height = 24 }) {
    if (!data || data.length < 2) {
        return null
    }

    // Normalize data to fit in the SVG
    const min = Math.min(...data)
    const max = Math.max(...data)
    const range = max - min || 1

    const padding = 2
    const chartWidth = width - padding * 2
    const chartHeight = height - padding * 2

    // Generate path points
    const points = data.map((value, index) => {
        const x = padding + (index / (data.length - 1)) * chartWidth
        const y = padding + chartHeight - ((value - min) / range) * chartHeight
        return `${x},${y}`
    })

    const pathD = `M ${points.join(' L ')}`

    // Color based on direction
    const colors = {
        rising: { stroke: '#34d399', fill: 'rgba(52, 211, 153, 0.2)' },
        falling: { stroke: '#94a3b8', fill: 'rgba(148, 163, 184, 0.1)' },
        stable: { stroke: '#fbbf24', fill: 'rgba(251, 191, 36, 0.15)' }
    }

    const { stroke, fill } = colors[direction] || colors.stable

    // Create area path (line + close to bottom)
    const areaD = `${pathD} L ${width - padding},${height - padding} L ${padding},${height - padding} Z`

    return (
        <svg
            width={width}
            height={height}
            className="inline-block"
            style={{ verticalAlign: 'middle' }}
        >
            {/* Gradient fill under the line */}
            <path
                d={areaD}
                fill={fill}
                opacity={0.5}
            />
            {/* The line itself */}
            <path
                d={pathD}
                fill="none"
                stroke={stroke}
                strokeWidth={1.5}
                strokeLinecap="round"
                strokeLinejoin="round"
            />
            {/* End point dot */}
            <circle
                cx={width - padding}
                cy={padding + chartHeight - ((data[data.length - 1] - min) / range) * chartHeight}
                r={2}
                fill={stroke}
            />
        </svg>
    )
}

export default TrendSparkline
