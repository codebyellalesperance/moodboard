function ProductCard({ product }) {
    const handleClick = () => {
        window.open(product.product_url, '_blank')
    }

    return (
        <div
            onClick={handleClick}
            className="bg-white rounded-xl overflow-hidden border border-gray-100 
                 hover:shadow-md transition-shadow cursor-pointer group"
        >
            {/* Image */}
            <div className="relative aspect-square bg-gray-100">
                <img
                    src={product.image_url}
                    alt={product.name}
                    className="w-full h-full object-cover"
                />
                {product.on_sale && (
                    <span className="absolute top-2 left-2 bg-red-500 text-white text-xs 
                          px-2 py-1 rounded-full font-medium">
                        SALE
                    </span>
                )}
            </div>

            {/* Info */}
            <div className="p-3">
                {/* Brand */}
                <p className="text-xs text-gray-400 uppercase tracking-wide">
                    {product.brand}
                </p>

                {/* Name */}
                <h3 className="text-sm text-gray-900 font-medium mt-1 line-clamp-2 
                       group-hover:underline">
                    {product.name}
                </h3>

                {/* Price */}
                <div className="mt-2 flex items-center gap-2">
                    <span className="font-semibold text-gray-900">
                        ${product.price}
                    </span>
                    {product.on_sale && product.original_price && (
                        <span className="text-sm text-gray-400 line-through">
                            ${product.original_price}
                        </span>
                    )}
                </div>

                {/* Retailer */}
                <p className="text-xs text-gray-400 mt-1">
                    {product.retailer}
                </p>
            </div>
        </div>
    )
}

export default ProductCard
