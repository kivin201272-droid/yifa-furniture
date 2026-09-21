/**
 * SofaCard.example.tsx
 * 
 * 示例 React + Tailwind 组件，演示如何从数据层读取沙发价格
 * 并通过 <PriceTag /> 组件动态渲染，与图片完全分离。
 * 
 * 使用方式:
 *   import sofaPrices from '../assets/data/sofa-prices.json'
 *   import { SofaCard } from './SofaCard'
 */

import React from 'react'

// ── Types ──────────────────────────────────────────────────────────────────

interface SofaPrices {
  chair?: number
  loveseat?: number
  sofa?: number
  sectional?: number
  sectional_4pc?: number
  ottoman?: number
  modular?: number
  modular_set?: number
  sofa_loveseat_ottoman?: number
  set?: number
  set_2plus3?: number
}

interface SofaProduct {
  model: string
  description_zh: string
  description_en: string
  material: string
  series: string
  prices: SofaPrices
}

// ── PriceTag Component ─────────────────────────────────────────────────────

interface PriceTagProps {
  prices: SofaPrices
  lang?: 'zh' | 'en'
}

const PRICE_LABELS_ZH: Record<keyof SofaPrices, string> = {
  chair: '单椅',
  loveseat: '双人位',
  sofa: '三人位',
  sectional: '转角组合',
  sectional_4pc: '四件套',
  ottoman: '脚踏',
  modular: '模块组合',
  modular_set: '模块套装',
  sofa_loveseat_ottoman: '沙发+双人+脚踏',
  set: '套装',
  set_2plus3: '2+3组合',
}

const PRICE_LABELS_EN: Record<keyof SofaPrices, string> = {
  chair: 'Chair',
  loveseat: 'Loveseat',
  sofa: 'Sofa',
  sectional: 'Sectional',
  sectional_4pc: 'Sectional (4pc)',
  ottoman: 'Ottoman',
  modular: 'Modular',
  modular_set: 'Modular Set',
  sofa_loveseat_ottoman: 'Sofa+Loveseat+Ottoman',
  set: 'Set',
  set_2plus3: '2+3 Set',
}

export function PriceTag({ prices, lang = 'zh' }: PriceTagProps) {
  const entries = Object.entries(prices).filter(([, v]) => v != null && v > 0)
  if (entries.length === 0) return null

  const labels = lang === 'zh' ? PRICE_LABELS_ZH : PRICE_LABELS_EN
  const badgeLabel = lang === 'zh' ? '特惠价' : 'Sale Price'

  const priceText = entries
    .map(([key, val]) => `${labels[key as keyof SofaPrices]}: $${val?.toLocaleString()}`)
    .join(' | ')

  return (
    <div className="inline-flex items-stretch rounded-md overflow-hidden shadow-sm border border-amber-800/20 text-sm mb-1 shrink-0">
      <span className="bg-amber-900 text-white text-[0.6rem] font-bold tracking-widest uppercase px-2.5 py-1.5 flex items-center whitespace-nowrap">
        {badgeLabel}
      </span>
      <span className="bg-amber-50 text-amber-950 font-semibold px-3 py-1.5 flex items-center whitespace-nowrap">
        {priceText}
      </span>
    </div>
  )
}

// ── SofaCard Component ─────────────────────────────────────────────────────

interface SofaCardProps {
  product: SofaProduct
  mainImage: string
  thumbnails?: string[]
  tags?: string[]
  lang?: 'zh' | 'en'
}

export function SofaCard({
  product,
  mainImage,
  thumbnails = [],
  tags = [],
  lang = 'zh',
}: SofaCardProps) {
  const [activeImg, setActiveImg] = React.useState(mainImage)
  const description = lang === 'zh' ? product.description_zh : product.description_en

  return (
    <article className="bg-white border border-stone-200 rounded-lg overflow-hidden flex flex-col transition-all duration-300 hover:-translate-y-1 hover:shadow-xl">
      {/* ── Product Image (clean, no price overlay) ── */}
      <div
        className="w-full aspect-[16/10] bg-gradient-to-br from-white to-stone-50 flex items-center justify-center overflow-hidden px-4 py-3"
        style={{ maxHeight: 360 }}
      >
        <img
          src={activeImg}
          alt={description}
          className="w-full h-full object-contain transition-transform duration-400 hover:scale-[1.02]"
          loading="lazy"
        />
      </div>

      {/* ── Thumbnails ── */}
      {thumbnails.length > 0 && (
        <div className="flex gap-2.5 px-4 py-3 bg-stone-50 border-b border-stone-100 flex-wrap">
          {[mainImage, ...thumbnails].map((src, i) => (
            <button
              key={i}
              onClick={() => setActiveImg(src)}
              className={`w-14 h-14 rounded border-2 overflow-hidden shrink-0 transition-all ${
                activeImg === src
                  ? 'border-amber-900 ring-2 ring-amber-900/30'
                  : 'border-stone-200 hover:border-amber-700'
              }`}
            >
              <img
                src={src}
                alt={`View ${i + 1}`}
                className="w-full h-full object-cover"
              />
            </button>
          ))}
        </div>
      )}

      {/* ── Product Info ── */}
      <div className="p-5 flex flex-col flex-grow">
        <h3 className="text-xl font-semibold text-stone-900 mb-2">{product.model}</h3>
        <p className="text-sm text-stone-600 leading-relaxed mb-4 flex-grow">{description}</p>

        {/* ── Price Badge — completely separate from image ── */}
        <div className="flex flex-wrap items-center gap-2 mt-auto pt-3">
          <PriceTag prices={product.prices} lang={lang} />
          {tags.map((tag) => (
            <span
              key={tag}
              className="text-[0.7rem] font-semibold text-amber-900 bg-amber-50 px-2.5 py-1 rounded uppercase tracking-wide"
            >
              {tag}
            </span>
          ))}
        </div>
      </div>
    </article>
  )
}

// ── Usage Example ──────────────────────────────────────────────────────────
//
// import sofaData from '../assets/data/sofa-prices.json'
//
// export default function LivingRoomPage() {
//   return (
//     <div className="grid grid-cols-2 gap-10 max-w-5xl mx-auto py-16 px-6">
//       {sofaData.filter(p => Object.keys(p.prices).length > 0).map(product => (
//         <SofaCard
//           key={product.model}
//           product={product}
//           mainImage={`/assets/images/living_room_named/${product.model}.jpg`}
//           tags={['精选']}
//           lang="zh"
//         />
//       ))}
//     </div>
//   )
// }

