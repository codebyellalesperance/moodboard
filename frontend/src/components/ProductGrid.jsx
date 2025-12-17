import ProductCard from './ProductCard'
import { ChevronDown, Shuffle, Loader2 } from 'lucide-react'

function ProductGrid({ products, displayedCount = 20, onLoadMore, onShuffle, isLoadingMore = false }) {
    if (!products?.length) return null

    const visibleProducts = products.slice(0, displayedCount)
    const hasMore = products.length > displayedCount
    const remainingCount = products.length - displayedCount

    return (
        <div className="space-y-8">
            {/* Shuffle Button */}
            {onShuffle && products.length > 1 && (
                <div className="flex justify-end">
                    <button
                        onClick={onShuffle}
                        className="group flex items-center gap-2 px-4 py-2 border border-[var(--border-color)] font-mono text-[10px] tracking-widest uppercase hover:border-[var(--color-text-primary)] hover:bg-[var(--color-text-primary)] hover:text-[var(--color-bg)] transition-all duration-300"
                    >
                        <Shuffle className="w-3 h-3 group-hover:rotate-180 transition-transform duration-500" />
                        <span>Shuffle</span>
                    </button>
                </div>
            )}

            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                {visibleProducts.map((product, index) => (
                    <ProductCard key={`${product.product_url}-${index}`} product={product} index={index} />
                ))}
            </div>

            {onLoadMore && (
                <div className="flex justify-center pt-4 border-t border-[var(--border-color)]">
                    <button
                        onClick={onLoadMore}
                        disabled={isLoadingMore}
                        className="group flex items-center gap-3 px-8 py-3 border border-[var(--color-text-primary)] font-mono text-xs tracking-widest uppercase hover:bg-[var(--color-text-primary)] hover:text-[var(--color-bg)] transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-transparent disabled:hover:text-inherit"
                    >
                        {isLoadingMore ? (
                            <>
                                <Loader2 className="w-4 h-4 animate-spin" />
                                <span>Curating More...</span>
                            </>
                        ) : (
                            <>
                                <span>Load More</span>
                                {hasMore && <span className="opacity-60">({Math.min(20, remainingCount)} cached)</span>}
                                <ChevronDown className="w-4 h-4 group-hover:translate-y-0.5 transition-transform" />
                            </>
                        )}
                    </button>
                </div>
            )}
        </div>
    )
}

export default ProductGrid
