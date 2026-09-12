export type VariantCode = 'T' | 'F' | 'Q' | 'Single' | 'Twin/Twin' | 'Full/Twin' | 'Twin/Full';

export type SizeName = 'Twin' | 'Full' | 'Queen' | 'Single' | 'Twin/Twin Bunk' | 'Full/Twin Bunk' | 'Twin/Full Bunk';

export interface ProductVariant {
  code: VariantCode | string;
  size: SizeName | string;
  price: number;
  originalPrice?: number;
  inStock?: boolean;
  sku?: string;
}

export interface Product {
  id: string;
  name: string;
  nameZh?: string;
  code?: string;
  category: 'Bed' | 'Bed Frame' | 'Bunk Bed' | 'Folding Bed' | 'Mattress' | 'Other';
  image?: string;
  description?: string;
  descriptionZh?: string;
  variants: ProductVariant[];
  featured?: boolean;
}

/**
 * Priority order for default size selection:
 * 1. Queen ('Q')
 * 2. Full ('F')
 * 3. Twin ('T')
 * 4. First available variant
 */
export function getDefaultVariant(variants: ProductVariant[]): ProductVariant {
  if (!variants || variants.length === 0) {
    return { code: 'Standard', size: 'Standard', price: 0 };
  }
  const queen = variants.find((v) => v.code === 'Q' || v.size.toLowerCase().includes('queen'));
  if (queen) return queen;

  const full = variants.find((v) => v.code === 'F' || v.size.toLowerCase().includes('full'));
  if (full) return full;

  const twin = variants.find((v) => v.code === 'T' || v.size.toLowerCase().includes('twin'));
  if (twin) return twin;

  return variants[0];
}

/**
 * Format numeric price to standard USD currency string (e.g., $159.00)
 */
export function formatPrice(price: number): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(price);
}
