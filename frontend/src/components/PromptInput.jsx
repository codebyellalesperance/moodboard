import { Wand2 } from 'lucide-react'

function PromptInput({ prompt, setPrompt }) {
    return (
        <div className="relative">
            <div className="absolute left-5 top-1/2 -translate-y-1/2">
                <Wand2 className="w-5 h-5 theme-text-tertiary" />
            </div>
            <input
                type="text"
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Describe your ideal vibe..."
                maxLength={200}
                className="w-full glass-card rounded-2xl pl-14 pr-20 py-5 theme-text-primary 
                     placeholder:theme-text-tertiary
                     focus:outline-none focus:border-[var(--glass-border-hover)] 
                     transition-all duration-400
                     text-base font-light"
            />
            <span className="absolute right-5 top-1/2 -translate-y-1/2 text-xs theme-text-tertiary 
                             px-2 py-1 rounded-full glass tabular-nums">
                {prompt.length}/200
            </span>
        </div>
    )
}

export default PromptInput
