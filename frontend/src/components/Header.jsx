import Clock from './Clock'
import ThemeToggle from './ThemeToggle'

function Header() {
    return (
        <header className="w-full mb-16 animate-fade-in relative z-50">
            {/* Top Bar - Tech/Meta info */}
            <div className="flex justify-between items-center py-2 border-b border-[var(--border-color)] text-xs font-mono tracking-widest text-[var(--color-text-secondary)] mb-8">
                <div className="flex items-center gap-4">
                    <span>EST. 2025</span>
                    <span>ISSUE NO. 01</span>
                </div>
                <div className="flex items-center gap-4">
                    <Clock />
                    <ThemeToggle />
                </div>
            </div>

            {/* Masthead */}
            <div className="text-center relative">
                <h1 className="text-[12vw] leading-[0.8] font-serif tracking-tighter text-[var(--color-text-primary)]">
                    MOODBOARD<span className="font-mono text-[2vw] tracking-normal align-top opacity-50 ml-2">TECH</span>
                </h1>

                {/* Decoration lines */}
                <div className="w-full h-px bg-[var(--color-text-primary)] mt-6 transform scale-x-0 animate-scale-in" style={{ animationDelay: '0.5s', animationFillMode: 'forwards' }} />
                <div className="w-full h-px bg-[var(--color-text-primary)] mt-1 transform scale-x-0 animate-scale-in" style={{ animationDelay: '0.6s', animationFillMode: 'forwards' }} />
            </div>
        </header>
    )
}

export default Header
