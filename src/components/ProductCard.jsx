import { ExternalLink } from 'lucide-react'

function ProductCard({ product }) {
    const handleClick = () => {
        window.open(product.product_url, '_blank')
    }

    return (
        <div
            onClick={handleClick}
            className="glass glass-hover rounded-xl overflow-hidden cursor-pointer group relative"
        >
            {/* Image */}
            <div className="relative aspect-[3/4] bg-white/5">
                <img
                    src={product.image_url}
                    alt={product.name}
                    className="w-full h-full object-cover opacity-90 group-hover:opacity-100 transition-opacity"
                />
                {product.on_sale && (
                    <span className="absolute top-2 left-2 bg-white text-black text-[10px] 
                          px-2 py-0.5 rounded-full font-medium tracking-wide uppercase">
                        Sale
                    </span>
                )}

                <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 
                        transition-opacity flex items-center justify-center backdrop-blur-[2px]">
                    <ExternalLink className="w-6 h-6 text-white" />
                </div>
            </div>

            {/* Info */}
            <div className="p-4 space-y-1">
                <p className="text-[10px] text-white/40 uppercase tracking-widest">
                    {product.brand}
                </p>

                <h3 className="text-sm text-white/90 font-light line-clamp-1">
                    {product.name}
                </h3>

                <div className="flex items-center gap-2 pt-1">
                    <span className="text-sm font-medium text-white">
                        ${product.price}
                    </span>
                    {product.on_sale && product.original_price && (
                        <span className="text-xs text-white/40 line-through decoration-white/20">
                            ${product.original_price}
                        </span>
                    )}
                </div>
            </div>
        </div>
    )
}

export default ProductCard
