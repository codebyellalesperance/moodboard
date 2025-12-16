import { useState, useMemo } from 'react'
import { SlidersHorizontal, X, ChevronDown, RefreshCw } from 'lucide-react'

const PRICE_RANGES = [
    { label: 'All Prices', min: 0, max: Infinity },
    { label: 'Under $25', min: 0, max: 25 },
    { label: '$25 - $50', min: 25, max: 50 },
    { label: '$50 - $100', min: 50, max: 100 },
    { label: '$100 - $200', min: 100, max: 200 },
    { label: '$200+', min: 200, max: Infinity }
]

const ITEM_TYPES = [
    { label: 'Tops', keywords: ['top', 'blouse', 'shirt', 'tee', 't-shirt', 'tank', 'sweater', 'hoodie', 'cardigan', 'pullover', 'cami', 'bodysuit'] },
    { label: 'Bottoms', keywords: ['pants', 'jeans', 'trousers', 'shorts', 'skirt', 'leggings'] },
    { label: 'Dresses', keywords: ['dress', 'gown', 'romper', 'jumpsuit', 'maxi', 'midi', 'mini dress'] },
    { label: 'Outerwear', keywords: ['jacket', 'coat', 'blazer', 'cardigan', 'vest', 'parka', 'puffer', 'trench'] },
    { label: 'Shoes', keywords: ['shoe', 'boot', 'sneaker', 'sandal', 'heel', 'flat', 'loafer', 'mule', 'slipper'] },
    { label: 'Bags', keywords: ['bag', 'purse', 'tote', 'clutch', 'backpack', 'crossbody', 'handbag', 'satchel'] },
    { label: 'Jewelry', keywords: ['necklace', 'earring', 'bracelet', 'ring', 'jewelry', 'chain', 'pendant'] },
    { label: 'Accessories', keywords: ['scarf', 'hat', 'belt', 'sunglasses', 'watch', 'hair', 'headband'] }
]

function ProductFilters({ products, filters, setFilters, onReloadWithFilter, isReloading }) {
    const [isOpen, setIsOpen] = useState(false)

    // Extract unique values from products
    const categories = useMemo(() => {
        const cats = [...new Set(products.map(p => p.category).filter(Boolean))]
        return cats.sort()
    }, [products])

    const brands = useMemo(() => {
        const b = [...new Set(products.map(p => p.brand).filter(Boolean))]
        return b.sort()
    }, [products])

    const retailers = useMemo(() => {
        const r = [...new Set(products.map(p => p.retailer).filter(Boolean))]
        return r.sort()
    }, [products])

    const activeFilterCount = [
        filters.priceRange?.label !== 'All Prices',
        filters.itemTypes?.length > 0,
        filters.categories?.length > 0,
        filters.brands?.length > 0,
        filters.retailers?.length > 0,
        filters.onSaleOnly
    ].filter(Boolean).length

    const clearFilters = () => {
        setFilters({
            priceRange: PRICE_RANGES[0],
            itemTypes: [],
            categories: [],
            brands: [],
            retailers: [],
            onSaleOnly: false
        })
    }

    const toggleArrayFilter = (key, value) => {
        const current = filters[key] || []
        const updated = current.includes(value)
            ? current.filter(v => v !== value)
            : [...current, value]
        setFilters({ ...filters, [key]: updated })
    }

    return (
        <div className="relative">
            {/* Toggle Button */}
            <button
                onClick={() => setIsOpen(!isOpen)}
                className={`flex items-center gap-2 px-4 py-2 rounded-xl glass transition-all duration-300 hover:bg-[var(--glass-bg-hover)] ${isOpen ? 'border-[var(--glass-border-hover)]' : ''}`}
            >
                <SlidersHorizontal className="w-4 h-4 theme-text-secondary" />
                <span className="text-sm font-medium theme-text-primary">Filters</span>
                {activeFilterCount > 0 && (
                    <span className="w-5 h-5 rounded-full bg-[var(--accent)] text-[var(--bg-primary)] text-xs font-bold flex items-center justify-center">
                        {activeFilterCount}
                    </span>
                )}
                <ChevronDown className={`w-4 h-4 theme-text-tertiary transition-transform duration-300 ${isOpen ? 'rotate-180' : ''}`} />
            </button>

            {/* Dark Backdrop */}
            {isOpen && (
                <div
                    className="fixed inset-0 bg-black/60 backdrop-blur-sm z-40"
                    onClick={() => setIsOpen(false)}
                />
            )}

            {/* Filter Panel */}
            {isOpen && (
                <div
                    className="absolute top-full right-0 mt-2 w-80 bg-[var(--bg-primary)] border border-[var(--border-color)] rounded-2xl p-4 space-y-4 z-50 animate-scale-in shadow-2xl"
                    onClick={(e) => e.stopPropagation()}
                >
                    {/* Header */}
                    <div className="flex items-center justify-between pb-2 border-b border-[var(--glass-border)]">
                        <span className="text-sm font-medium theme-text-primary">Filter Results</span>
                        {activeFilterCount > 0 && (
                            <button
                                onClick={clearFilters}
                                className="text-xs theme-text-tertiary hover:theme-text-primary transition-colors"
                            >
                                Clear all
                            </button>
                        )}
                    </div>

                    {/* Item Type */}
                    <div className="space-y-2">
                        <p className="text-xs font-medium theme-text-secondary uppercase tracking-wide">Item Type</p>
                        <div className="flex flex-wrap gap-1.5">
                            {ITEM_TYPES.map((type) => (
                                <button
                                    key={type.label}
                                    onClick={() => toggleArrayFilter('itemTypes', type.label)}
                                    className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-200 ${filters.itemTypes?.includes(type.label)
                                            ? 'bg-[var(--accent)] text-[var(--bg-primary)]'
                                            : 'bg-[var(--glass-bg)] hover:bg-[var(--glass-bg-hover)] theme-text-primary border border-[var(--border-color)]'
                                        }`}
                                >
                                    {type.label}
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* Price Range */}
                    <div className="space-y-2">
                        <p className="text-xs font-medium theme-text-secondary uppercase tracking-wide">Price</p>
                        <div className="flex flex-wrap gap-1.5">
                            {PRICE_RANGES.map((range) => (
                                <button
                                    key={range.label}
                                    onClick={() => setFilters({ ...filters, priceRange: range })}
                                    className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-200 ${filters.priceRange?.label === range.label
                                            ? 'bg-[var(--accent)] text-[var(--bg-primary)]'
                                            : 'bg-[var(--glass-bg)] hover:bg-[var(--glass-bg-hover)] theme-text-primary border border-[var(--border-color)]'
                                        }`}
                                >
                                    {range.label}
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* Category */}
                    {categories.length > 0 && (
                        <div className="space-y-2">
                            <p className="text-xs font-medium theme-text-secondary uppercase tracking-wide">Category</p>
                            <div className="flex flex-wrap gap-1.5 max-h-24 overflow-y-auto">
                                {categories.slice(0, 12).map((cat) => (
                                    <button
                                        key={cat}
                                        onClick={() => toggleArrayFilter('categories', cat)}
                                        className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-200 ${filters.categories?.includes(cat)
                                                ? 'bg-[var(--accent)] text-[var(--bg-primary)]'
                                                : 'glass hover:bg-[var(--glass-bg-hover)] theme-text-primary'
                                            }`}
                                    >
                                        {cat}
                                    </button>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* Retailer */}
                    {retailers.length > 0 && (
                        <div className="space-y-2">
                            <p className="text-xs font-medium theme-text-secondary uppercase tracking-wide">Retailer</p>
                            <div className="flex flex-wrap gap-1.5 max-h-24 overflow-y-auto">
                                {retailers.slice(0, 8).map((ret) => (
                                    <button
                                        key={ret}
                                        onClick={() => toggleArrayFilter('retailers', ret)}
                                        className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-200 ${filters.retailers?.includes(ret)
                                                ? 'bg-[var(--accent)] text-[var(--bg-primary)]'
                                                : 'glass hover:bg-[var(--glass-bg-hover)] theme-text-primary'
                                            }`}
                                    >
                                        {ret}
                                    </button>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* On Sale Toggle */}
                    <div className="flex items-center justify-between pt-2 border-t border-[var(--glass-border)]">
                        <span className="text-sm theme-text-primary">On Sale Only</span>
                        <button
                            onClick={() => setFilters({ ...filters, onSaleOnly: !filters.onSaleOnly })}
                            className={`w-10 h-6 rounded-full transition-all duration-300 ${filters.onSaleOnly
                                    ? 'bg-emerald-500'
                                    : 'bg-[var(--glass-bg)]'
                                }`}
                        >
                            <div className={`w-4 h-4 rounded-full bg-white shadow-md transition-transform duration-300 ${filters.onSaleOnly ? 'translate-x-5' : 'translate-x-1'
                                }`} />
                        </button>
                    </div>

                    {/* Reload with filter button */}
                    {filters.categories?.length === 1 && onReloadWithFilter && (
                        <button
                            onClick={() => {
                                onReloadWithFilter(filters.categories[0])
                                setIsOpen(false)
                            }}
                            disabled={isReloading}
                            className="w-full mt-2 py-2.5 rounded-xl bg-[var(--accent)] text-[var(--bg-primary)]
                                       text-sm font-medium flex items-center justify-center gap-2
                                       hover:opacity-90 transition-all duration-200 disabled:opacity-50"
                        >
                            <RefreshCw className={`w-4 h-4 ${isReloading ? 'animate-spin' : ''}`} />
                            {isReloading ? 'Loading...' : `Load 30 ${filters.categories[0]} items`}
                        </button>
                    )}

                    {filters.retailers?.length === 1 && onReloadWithFilter && (
                        <button
                            onClick={() => {
                                onReloadWithFilter(null, filters.retailers[0])
                                setIsOpen(false)
                            }}
                            disabled={isReloading}
                            className="w-full mt-2 py-2.5 rounded-xl bg-[var(--accent)] text-[var(--bg-primary)]
                                       text-sm font-medium flex items-center justify-center gap-2
                                       hover:opacity-90 transition-all duration-200 disabled:opacity-50"
                        >
                            <RefreshCw className={`w-4 h-4 ${isReloading ? 'animate-spin' : ''}`} />
                            {isReloading ? 'Loading...' : `Load 30 from ${filters.retailers[0]}`}
                        </button>
                    )}
                </div>
            )}
        </div>
    )
}

// Helper function to filter products
export function filterProducts(products, filters) {
    if (!products) return []

    return products.filter(product => {
        // Item type filter
        if (filters.itemTypes?.length > 0) {
            const productName = product.name || ''
            const matchesAny = filters.itemTypes.some(type => matchesItemType(productName, type))
            if (!matchesAny) return false
        }

        // Price filter
        if (filters.priceRange && filters.priceRange.label !== 'All Prices') {
            const price = product.price || 0
            if (price < filters.priceRange.min || price >= filters.priceRange.max) {
                return false
            }
        }

        // Category filter
        if (filters.categories?.length > 0) {
            if (!filters.categories.includes(product.category)) {
                return false
            }
        }

        // Brand filter
        if (filters.brands?.length > 0) {
            if (!filters.brands.includes(product.brand)) {
                return false
            }
        }

        // Retailer filter
        if (filters.retailers?.length > 0) {
            if (!filters.retailers.includes(product.retailer)) {
                return false
            }
        }

        // On sale filter
        if (filters.onSaleOnly && !product.on_sale) {
            return false
        }

        return true
    })
}

// Helper to check if product matches item type
function matchesItemType(productName, itemTypeLabel) {
    const itemType = ITEM_TYPES.find(t => t.label === itemTypeLabel)
    if (!itemType) return false
    const nameLower = productName.toLowerCase()
    return itemType.keywords.some(keyword => nameLower.includes(keyword))
}

export const DEFAULT_FILTERS = {
    priceRange: PRICE_RANGES[0],
    itemTypes: [],
    categories: [],
    brands: [],
    retailers: [],
    onSaleOnly: false
}

export default ProductFilters
