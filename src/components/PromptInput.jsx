function PromptInput({ prompt, setPrompt }) {
    return (
        <div className="space-y-3">
            <div className="relative">
                <input
                    type="text"
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    placeholder="DESCRIBE YOUR VIBE..."
                    maxLength={200}
                    className="w-full glass rounded-xl px-4 py-4 text-white placeholder-white/30 
                     focus:outline-none focus:border-white/30 transition-colors 
                     text-sm tracking-wide font-light"
                />
                <span className="absolute right-4 top-1/2 -translate-y-1/2 text-[10px] text-white/30">
                    {prompt.length}/200
                </span>
            </div>
        </div>
    )
}

export default PromptInput
