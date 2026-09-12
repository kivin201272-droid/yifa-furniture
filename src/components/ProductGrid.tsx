import React, { useState, useMemo } from 'react';
import { Product, ProductVariant } from '../types/product';
import { ProductCard } from './ProductCard';
import { ProductDetail } from './ProductDetail';

interface ProductGridProps {
  products: Product[];
  lang?: 'zh' | 'en';
}

export const ProductGrid: React.FC<ProductGridProps> = ({
  products,
  lang = 'zh',
}) => {
  const [selectedCategory, setSelectedCategory] = useState<string>('All');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [activeModalProduct, setActiveModalProduct] = useState<Product | null>(null);

  const categories = useMemo(() => {
    const cats = ['All', 'Bed', 'Bed Frame', 'Bunk Bed', 'Folding Bed'];
    return cats;
  }, []);

  const filteredProducts = useMemo(() => {
    return products.filter((p) => {
      const matchCat = selectedCategory === 'All' || p.category === selectedCategory;
      const q = searchQuery.toLowerCase().trim();
      const matchSearch =
        !q ||
        p.name.toLowerCase().includes(q) ||
        (p.nameZh && p.nameZh.toLowerCase().includes(q)) ||
        (p.code && p.code.toLowerCase().includes(q));
      return matchCat && matchSearch;
    });
  }, [products, selectedCategory, searchQuery]);

  return (
    <div className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      {/* Category Filter Tabs & Search Bar */}
      <div className="flex flex-col md:flex-row items-center justify-between gap-4 pb-8 border-b border-stone-200 dark:border-stone-800">
        {/* Category Pills */}
        <div className="flex flex-wrap items-center gap-2">
          {categories.map((cat) => {
            const isSelected = selectedCategory === cat;
            const labelZh: Record<string, string> = {
              All: '全部床品',
              Bed: '现代双人床',
              'Bed Frame': '金属/铁艺床架',
              'Bunk Bed': '双层上下铺',
              'Folding Bed': '折叠单人床',
            };
            return (
              <button
                key={cat}
                type="button"
                onClick={() => setSelectedCategory(cat)}
                className={`rounded-full px-4 py-2 text-xs md:text-sm font-semibold transition-all duration-200 ${
                  isSelected
                    ? 'bg-amber-800 text-white shadow-md shadow-amber-950/20'
                    : 'bg-stone-100 text-stone-600 hover:bg-stone-200 dark:bg-stone-800 dark:text-stone-300 dark:hover:bg-stone-700'
                }`}
              >
                {lang === 'zh' ? labelZh[cat] || cat : cat}
              </button>
            );
          })}
        </div>

        {/* Search Input */}
        <div className="relative w-full md:w-72">
          <input
            type="text"
            placeholder={lang === 'zh' ? '搜索型号 (如 7602, 7011, 7701)...' : 'Search code or name...'}
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full rounded-xl border border-stone-300 bg-white px-4 py-2.5 pl-10 text-xs md:text-sm text-stone-800 placeholder-stone-400 focus:border-amber-600 focus:outline-none focus:ring-2 focus:ring-amber-600/20 dark:border-stone-700 dark:bg-stone-900 dark:text-stone-100"
          />
          <svg
            className="absolute left-3.5 top-3 h-4 w-4 text-stone-400"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
      </div>

      {/* Product Results Count */}
      <div className="mt-4 flex items-center justify-between text-xs text-stone-500">
        <span>
          {lang === 'zh'
            ? `共找到 ${filteredProducts.length} 款现货床品规格`
            : `Showing ${filteredProducts.length} products`}
        </span>
      </div>

      {/* Grid of Product Cards */}
      <div className="mt-6 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {filteredProducts.map((product) => (
          <ProductCard
            key={product.id}
            product={product}
            lang={lang}
            onInquire={(p, v) => setActiveModalProduct(p)}
          />
        ))}
      </div>

      {/* Quick View Modal */}
      {activeModalProduct && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4 backdrop-blur-sm animate-fadeIn">
          <div className="relative w-full max-w-4xl">
            <ProductDetail
              product={activeModalProduct}
              lang={lang}
              onClose={() => setActiveModalProduct(null)}
            />
          </div>
        </div>
      )}
    </div>
  );
};
