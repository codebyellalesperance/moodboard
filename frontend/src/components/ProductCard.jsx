import { ExternalLink } from 'lucide-react'

function ProductCard({ product, index = 0 }) {
    const handleClick = () => {
        window.open(product.product_url, '_blank')
    }

    return (
        <div
            onClick={handleClick}
            className="group relative cursor-pointer animate-scale-in opacity-0"
            style={{ animationDelay: `${index * 0.08}s`, animationFillMode: 'forwards' }}
        >
            {/* Image Container */}
            <div className="relative aspect-[3/4] overflow-hidden bg-[var(--bg-secondary)] mb-4">
                <img
                    src={product.image_url}
                    alt={product.name}
                    className="w-full h-full object-cover transition-transform duration-700 ease-in-out group-hover:scale-105"
                />

                {/* Tech overlay on hover */}
                <div className="absolute inset-x-0 bottom-0 p-4 bg-gradient-to-t from-black/80 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                    <span className="inline-flex items-center gap-2 text-[10px] font-mono uppercase tracking-wider text-white border border-white/30 px-2 py-1">
                        View_Item <ExternalLink className="w-3 h-3" />
                    </span>
                </div>

                {/* Corners */}
                <div className="absolute top-0 left-0 w-2 h-2 border-t border-l border-transparent group-hover:border-[var(--color-text-primary)] transition-colors duration-300" />
                <div className="absolute top-0 right-0 w-2 h-2 border-t border-r border-transparent group-hover:border-[var(--color-text-primary)] transition-colors duration-300" />
                <div className="absolute bottom-0 left-0 w-2 h-2 border-b border-l border-transparent group-hover:border-[var(--color-text-primary)] transition-colors duration-300" />
                <div className="absolute bottom-0 right-0 w-2 h-2 border-b border-r border-transparent group-hover:border-[var(--color-text-primary)] transition-colors duration-300" />
            </div>

            {/* Typography */}
            <div className="space-y-1">
                <div className="flex justify-between items-baseline">
                    <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-[var(--color-text-secondary)]">
                        {product.brand}
                    </p>
                    {product.on_sale && product.original_price && (
                        <span className="font-mono text-[10px] text-red-500 line-through opacity-70">
                            ${product.original_price}
                        </span>
                    )}
                </div>

                <h3 className="font-sans text-sm font-light text-[var(--color-text-primary)] line-clamp-1 group-hover:underline decoration-1 underline-offset-4">
                    {product.name}
                </h3>

                <span className="block font-serif text-lg italic text-[var(--color-text-primary)]">
                    ${product.price}
                </span>
            </div>
        </div>
    )
}

export default ProductCard
