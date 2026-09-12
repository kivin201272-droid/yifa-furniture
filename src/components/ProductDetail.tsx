import React, { useState } from 'react';
import { Product, ProductVariant, getDefaultVariant, formatPrice } from '../types/product';

interface ProductDetailProps {
  product: Product;
  lang?: 'zh' | 'en';
  onClose?: () => void;
}

const SIZE_DIMENSIONS: Record<string, { in: string; cm: string }> = {
  Twin: { in: '39" × 75"', cm: '99 × 191 cm' },
  Full: { in: '54" × 75"', cm: '137 × 191 cm' },
  Queen: { in: '60" × 80"', cm: '152 × 203 cm' },
  Single: { in: '39" × 75" Foldable', cm: '99 × 191 cm 折叠' },
  'Twin/Twin': { in: 'Twin Over Twin', cm: '上下单人床' },
  'Full/Twin': { in: 'Full Over Twin', cm: '下双人+上单人' },
  'Twin/Full': { in: 'Twin Over Full', cm: '上单人+下双人' },
};

export const ProductDetail: React.FC<ProductDetailProps> = ({
  product,
  lang = 'zh',
  onClose,
}) => {
  const [selectedVariant, setSelectedVariant] = useState<ProductVariant>(() =>
    getDefaultVariant(product.variants)
  );

  const [quantity, setQuantity] = useState(1);
  const isMultiVariant = product.variants && product.variants.length > 1;

  const displayName = lang === 'zh' ? product.nameZh || product.name : product.name;
  const displayDesc = lang === 'zh' ? product.descriptionZh || product.description : product.description;

  const currentDimension = SIZE_DIMENSIONS[selectedVariant.size] || { in: 'Standard Spec', cm: '标准规格' };

  return (
    <div className="mx-auto max-w-5xl overflow-hidden rounded-2xl bg-white shadow-2xl dark:bg-stone-900 border border-stone-200 dark:border-stone-800">
      <div className="grid grid-cols-1 md:grid-cols-2">
        {/* Left: Product Image & Gallery */}
        <div className="relative flex items-center justify-center bg-stone-100 p-8 dark:bg-stone-800">
          <img
            src={product.image || '/assets/images/placeholder-bed.jpg'}
            alt={displayName}
            className="max-h-[420px] w-full object-contain drop-shadow-lg transition-transform duration-300 hover:scale-105"
          />
          {product.code && (
            <span className="absolute left-6 top-6 rounded-lg bg-stone-900/90 px-3 py-1.5 text-xs font-bold uppercase tracking-wider text-white backdrop-blur-md">
              SKU: {product.code}
            </span>
          )}
        </div>

        {/* Right: Product Details & Variant Configurator */}
        <div className="flex flex-col justify-between p-8 md:p-10">
          <div>
            {/* Header info */}
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold uppercase tracking-widest text-amber-700 dark:text-amber-500">
                {product.category}
              </span>
              {onClose && (
                <button
                  type="button"
                  onClick={onClose}
                  className="rounded-full p-1 text-stone-400 hover:bg-stone-100 hover:text-stone-700 dark:hover:bg-stone-800 dark:hover:text-stone-200"
                >
                  <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              )}
            </div>

            <h1 className="mt-2 text-2xl md:text-3xl font-black text-stone-900 dark:text-white">
              {displayName}
            </h1>

            <p className="mt-3 text-sm leading-relaxed text-stone-600 dark:text-stone-300">
              {displayDesc}
            </p>

            {/* Price Box */}
            <div className="mt-6 flex items-baseline gap-3 rounded-xl bg-stone-50 p-4 border border-stone-200/80 dark:bg-stone-800/50 dark:border-stone-700">
              <div className="flex flex-col">
                <span className="text-xs font-semibold text-stone-500">
                  {lang === 'zh' ? '批发优惠直供价' : 'Direct Wholesale Price'}
                </span>
                <span className="text-3xl font-extrabold text-red-600 dark:text-red-500">
                  {formatPrice(selectedVariant.price)}
                </span>
              </div>
              <span className="text-xs text-stone-400 line-through">
                {formatPrice(selectedVariant.price * 1.55)}
              </span>
              <span className="rounded bg-red-100 px-2 py-0.5 text-xs font-bold text-red-700 dark:bg-red-900/40 dark:text-red-300">
                -35% OFF
              </span>
            </div>

            {/* Specifications Selector */}
            {isMultiVariant && (
              <div className="mt-6">
                <label className="block text-xs font-bold uppercase tracking-wider text-stone-700 dark:text-stone-300">
                  {lang === 'zh' ? '选择规格尺寸 (Size)' : 'Select Size'}:{' '}
                  <span className="text-amber-700 dark:text-amber-400">
                    {selectedVariant.size} ({selectedVariant.code})
                  </span>
                </label>
                <div className="mt-2.5 grid grid-cols-3 gap-3">
                  {product.variants.map((v) => {
                    const isSelected = selectedVariant.code === v.code;
                    return (
                      <button
                        key={v.code}
                        type="button"
                        onClick={() => setSelectedVariant(v)}
                        className={`flex flex-col items-center justify-center rounded-xl border p-3.5 transition-all duration-200 active:scale-95 ${
                          isSelected
                            ? 'border-amber-700 bg-amber-50/80 text-amber-950 ring-2 ring-amber-700 dark:border-amber-500 dark:bg-amber-950/30 dark:text-amber-200'
                            : 'border-stone-200 bg-white text-stone-700 hover:border-stone-300 hover:bg-stone-50 dark:border-stone-700 dark:bg-stone-800 dark:text-stone-300'
                        }`}
                      >
                        <span className="text-sm font-extrabold">{v.code}</span>
                        <span className="text-[11px] text-stone-500 dark:text-stone-400">{v.size}</span>
                        <span className="mt-1 text-xs font-bold text-red-600 dark:text-red-400">
                          {formatPrice(v.price)}
                        </span>
                      </button>
                    );
                  })}
                </div>
              </div>
            )}

            {/* Dimensions Info */}
            <div className="mt-5 rounded-lg border border-dashed border-stone-200 p-3 text-xs text-stone-500 dark:border-stone-700 dark:text-stone-400">
              <span className="font-semibold text-stone-700 dark:text-stone-300">
                {lang === 'zh' ? '参考尺寸' : 'Dimensions'}:{' '}
              </span>
              {currentDimension.in} ({currentDimension.cm})
            </div>
          </div>

          {/* Bottom Actions */}
          <div className="mt-8 flex flex-col gap-3 sm:flex-row">
            <a
              href="tel:+19177715493"
              className="flex flex-1 items-center justify-center gap-2 rounded-xl bg-amber-700 px-6 py-3.5 text-sm font-bold uppercase tracking-wider text-white shadow-lg shadow-amber-900/20 transition-all duration-200 hover:bg-amber-800 active:scale-95"
            >
              <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
              </svg>
              <span>{lang === 'zh' ? '电话订购：917-771-5493' : 'Call 917-771-5493'}</span>
            </a>
            <a
              href={`mailto:Wilson8888huang@gmail.com?subject=Inquiry for ${product.name} (${selectedVariant.size})`}
              className="flex items-center justify-center rounded-xl border border-stone-300 bg-white px-5 py-3.5 text-sm font-bold text-stone-700 transition-all duration-200 hover:bg-stone-50 dark:border-stone-700 dark:bg-stone-800 dark:text-stone-200"
            >
              {lang === 'zh' ? '邮件咨询' : 'Email Us'}
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};
