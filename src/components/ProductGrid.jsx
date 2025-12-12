import ProductCard from './ProductCard'

function ProductGrid({ products }) {
    if (!products || products.length === 0) {
        return (
            <div className="text-center py-12 text-gray-400">
                No products found. Try different images or adjust your prompt.
            </div>
        )
    }

    return (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {products.map((product) => (
                <ProductCard key={product.id} product={product} />
            ))}
        </div>
    )
}

export default ProductGrid
