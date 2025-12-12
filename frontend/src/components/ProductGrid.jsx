import ProductCard from './ProductCard'

function ProductGrid({ products }) {
    if (!products?.length) return null

    return (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            {products.map((product, index) => (
                <ProductCard key={product.product_url || index} product={product} index={index} />
            ))}
        </div>
    )
}

export default ProductGrid
