/**
 * TypeScript definitions for @canonical/image-template
 */

export interface ImageTemplateOptions {
  /** Image URL */
  url: string;
  /** Alt text for accessibility */
  alt: string;
  /** Primary image width */
  width: number;
  /** Image height (optional) */
  height?: number | null;
  /** Whether to crop and fill to exact dimensions */
  fill?: boolean;
  /** Whether to apply sharpening */
  eSharpen?: boolean;
  /** Loading strategy */
  loading?: 'lazy' | 'eager' | 'auto';
  /** Image format */
  fmt?: string;
  /** Additional HTML attributes */
  attrs?: Record<string, string | number | boolean>;
  /** Responsive sizes attribute template */
  sizes?: string;
  /** Custom widths for srcset generation */
  srcsetWidths?: number[];
  /** Enable high-DPI support (up to 2x) */
  hiDef?: boolean;
}

export interface ImageAttributes {
  src: string;
  srcset?: string;
  sizes?: string;
  alt: string;
  width: number;
  height?: number | null;
  loading: string;
  [key: string]: string | number | boolean | null | undefined;
}

/**
 * Generate responsive image attributes for Cloudinary integration
 * @param options - Image template options
 * @returns Image attributes object
 */
export declare function imageTemplate(options: ImageTemplateOptions): ImageAttributes;

// Default export for CommonJS compatibility
export = { imageTemplate };