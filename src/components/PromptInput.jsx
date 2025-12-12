function PromptInput({ prompt, setPrompt }) {
    const maxLength = 200

    const examplePrompts = [
        "But affordable",
        "For summer",
        "Work appropriate",
        "Date night",
        "Casual version"
    ]

    const addToPrompt = (text) => {
        const newPrompt = prompt ? `${prompt} ${text}`.trim() : text
        if (newPrompt.length <= maxLength) {
            setPrompt(newPrompt)
        }
    }

    return (
        <div className="w-full">
            <div className="relative">
                <input
                    type="text"
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value.slice(0, maxLength))}
                    placeholder="Describe what you want (optional) — e.g., 'This but affordable'"
                    className="w-full px-4 py-3 rounded-xl border border-gray-200 bg-white
                     focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent
                     text-gray-900 placeholder-gray-400"
                />
                <span className="absolute right-3 top-1/2 -translate-y-1/2 text-xs text-gray-400">
                    {prompt.length}/{maxLength}
                </span>
            </div>

            {/* Example prompt chips */}
            <div className="mt-3 flex flex-wrap gap-2">
                {examplePrompts.map((example) => (
                    <button
                        key={example}
                        onClick={() => addToPrompt(example)}
                        className="px-3 py-1 text-sm bg-gray-100 hover:bg-gray-200 
                       rounded-full text-gray-600 transition-colors"
                    >
                        {example}
                    </button>
                ))}
            </div>
        </div>
    )
}

export default PromptInput
