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
 * Image Template class for generating responsive image attributes
 */
export declare class ImageTemplate {
  constructor();
  
  /**
   * Generate responsive image attributes with optimized srcset and sizes
   */
  imageTemplate(options: ImageTemplateOptions): ImageAttributes;
  
  /**
   * Render HTML string from image attributes
   */
  renderHtml(imageAttrs: ImageAttributes): string;
  
  /**
   * Escape HTML special characters
   */
  escapeHtml(text: string): string;
}

/**
 * Convenience function that matches the Python API
 */
export declare function imageTemplate(options: ImageTemplateOptions): ImageAttributes;

// Default export for CommonJS compatibility
export { ImageTemplate as default };