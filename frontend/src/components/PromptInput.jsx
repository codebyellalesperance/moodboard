import { Terminal, CornerDownLeft } from 'lucide-react'

function PromptInput({ prompt, setPrompt, onSubmit, canSubmit }) {
    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey && canSubmit) {
            e.preventDefault()
            onSubmit()
        }
    }

    return (
        <div className="w-full">
            <div className="flex items-center gap-2 mb-1 sm:mb-2 opacity-70">
                <Terminal className="w-3 h-3 text-[var(--color-text-secondary)]" />
                <span className="font-mono text-[10px] sm:text-xs tracking-widest uppercase text-[var(--color-text-secondary)]">
                    Aesthetic Input_
                </span>
            </div>

            <div className="relative group">
                <div className="absolute top-0 left-0 w-2 h-2 border-t border-l border-[var(--color-text-primary)] transition-all group-focus-within:w-4 group-focus-within:h-4" />
                <div className="absolute top-0 right-0 w-2 h-2 border-t border-r border-[var(--color-text-primary)] transition-all group-focus-within:w-4 group-focus-within:h-4" />
                <div className="absolute bottom-0 left-0 w-2 h-2 border-b border-l border-[var(--color-text-primary)] transition-all group-focus-within:w-4 group-focus-within:h-4" />
                <div className="absolute bottom-0 right-0 w-2 h-2 border-b border-r border-[var(--color-text-primary)] transition-all group-focus-within:w-4 group-focus-within:h-4" />

                <textarea
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="// Describe aesthetic parameters, e.g. 'Cyberpunk concrete jungle' or '90s minimalist tech'..."
                    maxLength={500}
                    rows={3}
                    className="w-full bg-[var(--bg-secondary)] text-[var(--color-text-primary)]
                         placeholder:text-[var(--color-text-secondary)] placeholder:opacity-40
                         focus:outline-none focus:bg-[var(--bg-secondary)]
                         text-sm sm:text-base lg:text-lg font-light leading-relaxed p-3 sm:p-4 lg:p-6
                         border-l border-r border-[var(--border-color)]"
                />
            </div>

            <div className="flex justify-between items-center mt-1 sm:mt-2 px-1">
                <span className="font-mono text-[9px] sm:text-[10px] text-[var(--color-text-secondary)]">
                    MAX_CHARS: 500
                </span>
                <div className="flex items-center gap-2">
                    <span className="font-mono text-[9px] sm:text-[10px] text-[var(--color-text-secondary)]">
                        {prompt.length} / 500
                    </span>
                    {canSubmit && (
                        <span className="font-mono text-[9px] sm:text-[10px] text-[var(--color-accent)] animate-pulse">
                            [READY]
                        </span>
                    )}
                </div>
            </div>
        </div>
    )
}

export default PromptInput
