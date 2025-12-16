import ProductCard from './ProductCard'
import { ChevronDown } from 'lucide-react'

function ProductGrid({ products, displayedCount = 20, onLoadMore }) {
    if (!products?.length) return null

    const visibleProducts = products.slice(0, displayedCount)
    const hasMore = products.length > displayedCount
    const remainingCount = products.length - displayedCount

    return (
        <div className="space-y-8">
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                {visibleProducts.map((product, index) => (
                    <ProductCard key={product.product_url || index} product={product} index={index} />
                ))}
            </div>

            {hasMore && onLoadMore && (
                <div className="flex justify-center pt-4 border-t border-[var(--border-color)]">
                    <button
                        onClick={onLoadMore}
                        className="group flex items-center gap-3 px-8 py-3 border border-[var(--color-text-primary)] font-mono text-xs tracking-widest uppercase hover:bg-[var(--color-text-primary)] hover:text-[var(--color-bg)] transition-all duration-300"
                    >
                        <span>Load More</span>
                        <span className="opacity-60">({Math.min(20, remainingCount)} more)</span>
                        <ChevronDown className="w-4 h-4 group-hover:translate-y-0.5 transition-transform" />
                    </button>
                </div>
            )}
        </div>
    )
}

export default ProductGrid
