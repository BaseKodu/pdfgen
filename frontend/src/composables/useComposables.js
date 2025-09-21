const BUTTON_VARIANTS = {
  NEUTRAL: 'neutral',
  PRIMARY: 'primary',
  SECONDARY: 'secondary',
  ACCENT: 'accent',
  INFO: 'info',
  SUCCESS: 'success',
  WARNING: 'warning',
  ERROR: 'error',
  OUTLINE: 'outline',
  DASH: 'dash',
  SOFT: 'soft',
  GHOST: 'ghost',
  LINK: 'link'
}

const BUTTON_VARIANT_VALUES = Object.values(BUTTON_VARIANTS)

export const useButtonVariants = () => {
  return {
    variant: {
      type: String,
      default: 'primary',
      validator: (value) => BUTTON_VARIANT_VALUES.includes(value)
    }
  }
}

export { BUTTON_VARIANTS, BUTTON_VARIANT_VALUES }
