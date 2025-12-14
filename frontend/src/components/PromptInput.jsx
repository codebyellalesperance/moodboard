import { Sparkles, CornerDownLeft } from 'lucide-react'

function PromptInput({ prompt, setPrompt, onSubmit, canSubmit }) {
    const handleKeyDown = (e) => {
        // Submit on Enter (without Shift for newlines)
        if (e.key === 'Enter' && !e.shiftKey && canSubmit) {
            e.preventDefault()
            onSubmit()
        }
    }

    return (
        <div className="relative">
            {/* Decorative gradient border effect */}
            <div className="absolute -inset-[1px] bg-gradient-to-r from-[var(--accent)]/20 via-[var(--accent-muted)]/10 to-[var(--accent)]/20 rounded-3xl blur-sm opacity-0 group-focus-within:opacity-100 transition-opacity duration-500" />

            <div className="relative glass-card rounded-3xl p-6 group focus-within:border-[var(--glass-border-hover)] transition-all duration-500">
                {/* Header */}
                <div className="flex items-center gap-3 mb-4">
                    <div className="w-10 h-10 rounded-xl glass flex items-center justify-center">
                        <Sparkles className="w-5 h-5 theme-text-secondary" />
                    </div>
                    <div>
                        <h3 className="text-sm font-medium theme-text-primary">Describe Your Vibe</h3>
                        <p className="text-xs theme-text-tertiary">What aesthetic are you going for?</p>
                    </div>
                </div>

                {/* Textarea */}
                <textarea
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="e.g., coastal grandmother meets quiet luxury, or 90s minimalist with earth tones, or dark academia for fall..."
                    maxLength={500}
                    rows={4}
                    className="w-full bg-transparent theme-text-primary
                         placeholder:theme-text-tertiary placeholder:text-sm
                         focus:outline-none resize-none
                         text-base font-light leading-relaxed"
                />

                {/* Footer */}
                <div className="flex items-center justify-between mt-3 pt-3 border-t border-[var(--glass-border)]">
                    <span className="text-xs theme-text-tertiary">
                        Add images for better results, or just describe your vibe
                    </span>
                    <div className="flex items-center gap-3">
                        {canSubmit && (
                            <span className="flex items-center gap-1.5 text-xs theme-text-tertiary opacity-60">
                                <CornerDownLeft className="w-3 h-3" />
                                to submit
                            </span>
                        )}
                        <span className="text-xs theme-text-tertiary tabular-nums px-2 py-1 rounded-full glass">
                            {prompt.length}/500
                        </span>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default PromptInput
