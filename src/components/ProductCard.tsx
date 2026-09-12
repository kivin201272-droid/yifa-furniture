import React, { useState } from 'react';
import { Product, ProductVariant, getDefaultVariant, formatPrice } from '../types/product';

interface ProductCardProps {
  product: Product;
  lang?: 'zh' | 'en';
  onInquire?: (product: Product, selectedVariant: ProductVariant) => void;
  tags?: string[];
}

export const ProductCard: React.FC<ProductCardProps> = ({
  product,
  lang = 'zh',
  onInquire,
  tags = [],
}) => {
  const [selectedVariant, setSelectedVariant] = useState<ProductVariant>(() =>
    getDefaultVariant(product.variants)
  );

  const isMultiVariant = product.variants && product.variants.length > 1;

  const handleSelectVariant = (variant: ProductVariant) => {
    setSelectedVariant(variant);
  };

  const handleInquireClick = () => {
    if (onInquire) {
      onInquire(product, selectedVariant);
    } else {
      window.location.href = `tel:+19177715493`;
    }
  };

  const displayName = lang === 'zh' ? product.nameZh || product.name : product.name;
  const displayDesc = lang === 'zh' ? product.descriptionZh || product.description : product.description;
  const isZh = lang === 'zh';
  const prefix = isZh ? '折后' : 'Sale ';

  return (
    <div className="group relative flex flex-col overflow-hidden rounded-2xl border border-stone-200 bg-white shadow-sm transition-all duration-300 hover:-translate-y-1 hover:shadow-xl hover:border-amber-700/30 dark:border-stone-800 dark:bg-stone-900">
      {/* 1. Pure Clean Image Container (No floating overlays) */}
      <div className="relative aspect-[4/3] w-full overflow-hidden bg-stone-100 dark:bg-stone-800">
        <img
          src={product.image || '/assets/images/placeholder-bed.jpg'}
          alt={displayName}
          loading="lazy"
          className="h-full w-full object-cover object-center transition-transform duration-500 ease-out group-hover:scale-105"
        />

        {/* Badges (Top Left) */}
        <div className="absolute left-3 top-3 z-10 flex flex-wrap gap-1.5">
          {product.code && (
            <span className="rounded-md bg-stone-900/80 px-2.5 py-1 text-xs font-semibold tracking-wider text-white backdrop-blur-md dark:bg-stone-100/90 dark:text-stone-900 shadow-sm">
              {product.code}
            </span>
          )}
          {product.featured && (
            <span className="rounded-md bg-amber-600 px-2 py-1 text-xs font-bold uppercase tracking-wider text-white shadow-sm">
              {isZh ? '热销' : 'Popular'}
            </span>
          )}
        </div>
      </div>

      {/* 2. Card Content Body */}
      <div className="flex flex-1 flex-col p-5">
        {/* Title */}
        <h3 className="line-clamp-1 text-base md:text-lg font-bold text-stone-900 transition-colors group-hover:text-amber-700 dark:text-stone-100 dark:group-hover:text-amber-400">
          {displayName}
        </h3>

        {/* Description */}
        {displayDesc && (
          <p className="mt-1.5 line-clamp-2 text-xs leading-relaxed text-stone-500 dark:text-stone-400">
            {displayDesc}
          </p>
        )}

        {/* 3. Bottom Price Bar & Badges (Aligns exactly with existing template style) */}
        <div className="mt-4 flex flex-wrap items-center gap-2 border-t border-stone-100 pt-3 dark:border-stone-800">
          {isMultiVariant ? (
            <div className="inline-flex flex-wrap items-center gap-1.5 text-xs">
              <span className="font-extrabold text-red-600 dark:text-red-500 text-sm">
                {prefix}
              </span>
              {product.variants.map((v, idx) => {
                const isQueen = v.code === 'Q' || (v.size && v.size.toLowerCase().includes('queen'));
                const isSelected = selectedVariant.code === v.code;
                const formattedPrice = Number.isInteger(v.price) ? `$${v.price}` : `$${v.price.toFixed(2)}`;

                return (
                  <React.Fragment key={v.code || idx}>
                    {idx > 0 && <span className="text-stone-300 dark:text-stone-700">|</span>}
                    <button
                      type="button"
                      onClick={() => handleSelectVariant(v)}
                      className={`inline-flex items-center gap-1 rounded px-2 py-0.5 text-xs font-bold transition-all ${
                        isQueen || isSelected
                          ? 'bg-amber-100 text-amber-900 border border-amber-300 dark:bg-amber-950/60 dark:text-amber-300 dark:border-amber-800 shadow-sm'
                          : 'bg-stone-100 text-stone-800 border border-stone-200 dark:bg-stone-800 dark:text-stone-300 dark:border-stone-700 hover:bg-stone-200'
                      }`}
                      title={`${v.size}: ${formattedPrice}`}
                    >
                      <span className="text-stone-500 dark:text-stone-400 font-normal">{v.code}</span>
                      <span className={isQueen || isSelected ? 'text-amber-800 dark:text-amber-300' : 'text-red-600 dark:text-red-400'}>
                        {formattedPrice}
                      </span>
                    </button>
                  </React.Fragment>
                );
              })}
            </div>
          ) : (
            <div className="inline-flex items-baseline gap-1">
              <span className="text-lg font-black text-red-600 dark:text-red-500">
                {prefix}{formatPrice(selectedVariant.price)}
              </span>
            </div>
          )}

          {/* Additional Detail Tags */}
          {tags.map((tag, idx) => (
            <span
              key={idx}
              className="rounded bg-stone-100 px-2 py-0.5 text-[11px] font-semibold uppercase tracking-wider text-amber-800 dark:bg-stone-800 dark:text-amber-400"
            >
              {tag}
            </span>
          ))}
        </div>

        {/* 4. Action Button Footer */}
        <div className="mt-4 flex items-center justify-between border-t border-stone-100 pt-3 dark:border-stone-800">
          <span className="text-xs text-stone-500">
            {isZh ? '当前所选: ' : 'Selected: '}
            <strong className="text-stone-800 dark:text-stone-200 font-bold">
              {selectedVariant.size} ({formatPrice(selectedVariant.price)})
            </strong>
          </span>

          <button
            type="button"
            onClick={handleInquireClick}
            className="flex items-center justify-center rounded-lg bg-stone-900 px-3.5 py-2 text-xs font-bold uppercase tracking-wider text-white transition-all duration-200 hover:bg-amber-700 hover:shadow-md active:scale-95 dark:bg-stone-100 dark:text-stone-900 dark:hover:bg-amber-500"
          >
            {isZh ? '立即咨询' : 'Inquire'}
          </button>
        </div>
      </div>
    </div>
  );
};
