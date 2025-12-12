import { Sun, Moon } from 'lucide-react'
import { useTheme } from '../context/ThemeContext'

function ThemeToggle() {
    const { theme, toggleTheme } = useTheme()
    const isDark = theme === 'dark'

    return (
        <button
            onClick={toggleTheme}
            aria-label={`Switch to ${isDark ? 'light' : 'dark'} mode`}
            className="relative w-11 h-11 rounded-xl glass glass-hover
                       flex items-center justify-center overflow-hidden group"
        >
            <div className={`absolute transition-all duration-500 ease-out
                            ${isDark ? 'rotate-0 opacity-100 scale-100' : 'rotate-90 opacity-0 scale-50'}`}>
                <Moon className="w-5 h-5 theme-text-secondary group-hover:theme-text-primary transition-colors" />
            </div>
            <div className={`absolute transition-all duration-500 ease-out
                            ${isDark ? '-rotate-90 opacity-0 scale-50' : 'rotate-0 opacity-100 scale-100'}`}>
                <Sun className="w-5 h-5 theme-text-secondary group-hover:theme-text-primary transition-colors" />
            </div>
        </button>
    )
}

export default ThemeToggle
