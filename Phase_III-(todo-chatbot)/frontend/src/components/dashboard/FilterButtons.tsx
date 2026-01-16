'use client';

import { motion, useReducedMotion } from 'framer-motion';
import { Button } from '@/components/ui/button';

export type FilterType = 'all' | 'pending' | 'completed';

interface FilterButtonsProps {
  activeFilter: FilterType;
  onFilterChange: (filter: FilterType) => void;
}

const FilterButtons = ({ activeFilter, onFilterChange }: FilterButtonsProps) => {
  const shouldReduceMotion = useReducedMotion();

  const filters: { label: string; value: FilterType }[] = [
    { label: 'All', value: 'all' },
    { label: 'Active', value: 'pending' },
    { label: 'Completed', value: 'completed' },
  ];

  return (
    <div className="flex flex-wrap gap-3 mb-6">
      {filters.map((filter) => (
        <motion.div
          key={filter.value}
          whileHover={shouldReduceMotion ? {} : { y: -2, scale: 1.05 }}
          whileTap={shouldReduceMotion ? {} : { scale: 0.95 }}
          transition={{ type: 'spring', stiffness: 400 }}
        >
          <Button
            onClick={() => onFilterChange(filter.value)}
            variant={activeFilter === filter.value ? 'default' : 'ghost'}
            className={`
              px-6 py-2 rounded-lg font-medium transition-all duration-200
              ${
                activeFilter === filter.value
                  ? 'bg-gradient-to-r from-primary-purple to-primary-blue text-white shadow-lg'
                  : 'glass-card text-white/80 hover:text-white hover:bg-white/10'
              }
            `}
          >
            {filter.label}
          </Button>
        </motion.div>
      ))}
    </div>
  );
};

export default FilterButtons;
