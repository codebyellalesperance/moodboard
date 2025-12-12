import { ExternalLink } from 'lucide-react'

function ProductCard({ product, index = 0 }) {
    const handleClick = () => {
        window.open(product.product_url, '_blank')
    }

    return (
        <div
            onClick={handleClick}
            className="glass-card rounded-2xl overflow-hidden cursor-pointer group relative
                       animate-scale-in opacity-0"
            style={{ animationDelay: `${index * 0.08}s`, animationFillMode: 'forwards' }}
        >
            {/* Image */}
            <div className="relative aspect-[3/4] bg-[var(--bg-secondary)] overflow-hidden">
                <img
                    src={product.image_url}
                    alt={product.name}
                    className="w-full h-full object-cover 
                               group-hover:scale-110 transition-all duration-700 ease-out"
                />

                {/* Gradient overlay on hover */}
                <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-black/20 to-transparent 
                                opacity-0 group-hover:opacity-100 transition-all duration-400" />

                {product.on_sale && (
                    <span className="absolute top-3 left-3 bg-gradient-to-r from-rose-500 to-pink-500 
                          text-white text-[10px] px-3 py-1.5 rounded-full font-semibold tracking-wider uppercase
                          shadow-lg">
                        Sale
                    </span>
                )}

                <div className="absolute bottom-4 left-1/2 -translate-x-1/2
                                opacity-0 group-hover:opacity-100 group-hover:translate-y-0 translate-y-4
                                transition-all duration-400">
                    <div className="flex items-center gap-2 px-4 py-2 rounded-full 
                                    bg-white/90 backdrop-blur-sm text-black text-xs font-medium">
                        <span>View Product</span>
                        <ExternalLink className="w-3 h-3" />
                    </div>
                </div>
            </div>

            {/* Info */}
            <div className="p-5 space-y-2">
                <p className="text-[10px] theme-text-tertiary uppercase tracking-[0.15em] font-medium">
                    {product.brand}
                </p>

                <h3 className="text-sm theme-text-primary font-medium line-clamp-1">
                    {product.name}
                </h3>

                <div className="flex items-center gap-3 pt-1">
                    <span className="text-base font-semibold theme-accent">
                        ${product.price}
                    </span>
                    {product.on_sale && product.original_price && (
                        <span className="text-sm theme-text-tertiary line-through">
                            ${product.original_price}
                        </span>
                    )}
                </div>
            </div>
        </div>
    )
}

export default ProductCard
