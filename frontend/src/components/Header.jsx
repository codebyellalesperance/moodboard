import Clock from './Clock'
import ThemeToggle from './ThemeToggle'

function Header() {
    return (
        <header className="py-8 animate-fade-in">
            <div className="flex items-center justify-between">
                {/* Clock - Left */}
                <div className="w-32">
                    <div className="glass inline-flex px-4 py-2 rounded-full">
                        <Clock />
                    </div>
                </div>

                {/* Logo/Title - Center */}
                <div className="flex flex-col items-center gap-1">
                    <h1 className="text-xl font-light tracking-[0.4em] theme-text-primary uppercase">
                        Moodboard
                    </h1>
                    <div className="w-12 h-[1px] bg-gradient-to-r from-transparent via-[var(--text-tertiary)] to-transparent" />
                </div>

                {/* Theme Toggle - Right */}
                <div className="w-32 flex justify-end">
                    <ThemeToggle />
                </div>
            </div>
        </header>
    )
}

export default Header
