import { Variants } from 'framer-motion';

// Fade in animation variant
export const fadeIn: Variants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { duration: 0.3 } },
};

// Slide up animation variant
export const slideUp: Variants = {
  hidden: { y: 20, opacity: 0 },
  visible: { y: 0, opacity: 1, transition: { duration: 0.3 } },
};

// Stagger animation variant for children
export const stagger: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
    },
  },
};

// Hover lift animation variant
export const hoverLift: Variants = {
  hover: {
    y: -4,
    scale: 1.02,
    transition: { duration: 0.2, ease: 'easeInOut' },
  },
  tap: {
    scale: 0.98,
    transition: { duration: 0.1 },
  },
};

// Scale in with bounce animation
export const scaleInBounce: Variants = {
  hidden: { scale: 0 },
  visible: {
    scale: 1,
    transition: {
      type: 'spring',
      stiffness: 300,
      damping: 15
    }
  },
};

// Fade out animation
export const fadeOut: Variants = {
  visible: { opacity: 1 },
  hidden: { opacity: 0, transition: { duration: 0.3 } },
};