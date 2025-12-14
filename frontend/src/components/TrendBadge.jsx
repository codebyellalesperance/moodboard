import { TrendingUp, TrendingDown, Minus, HelpCircle } from 'lucide-react'

function TrendBadge({ trend }) {
    if (!trend || trend.direction === 'unknown') {
        return null
    }

    const config = {
        rising: {
            icon: TrendingUp,
            label: 'Rising',
            bgClass: 'bg-emerald-500/20 border-emerald-500/30',
            textClass: 'text-emerald-400',
            iconClass: 'text-emerald-400'
        },
        falling: {
            icon: TrendingDown,
            label: 'Cooling off',
            bgClass: 'bg-slate-500/20 border-slate-500/30',
            textClass: 'text-slate-400',
            iconClass: 'text-slate-400'
        },
        stable: {
            icon: Minus,
            label: 'Steady',
            bgClass: 'bg-amber-500/20 border-amber-500/30',
            textClass: 'text-amber-400',
            iconClass: 'text-amber-400'
        }
    }

    const { icon: Icon, label, bgClass, textClass, iconClass } = config[trend.direction] || config.stable

    return (
        <div className={`inline-flex items-center gap-2 px-3 py-1.5 rounded-full border ${bgClass} transition-all duration-300 hover:scale-105`}>
            <Icon className={`w-3.5 h-3.5 ${iconClass}`} />
            <span className={`text-xs font-medium tracking-wide ${textClass}`}>
                {label}
            </span>
            {trend.change && (
                <span className={`text-xs font-semibold ${textClass}`}>
                    {trend.change}
                </span>
            )}
        </div>
    )
}

export default TrendBadge
