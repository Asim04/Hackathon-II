import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { motion } from 'framer-motion';

import { UseFormRegister } from 'react-hook-form';
import { SignUpInput, SignInInput } from '../../lib/schemas';

// Accept all possible field names from both schemas
type FormFieldId = keyof SignUpInput | keyof SignInInput;

interface FormFieldProps {
  id: FormFieldId;
  label: string;
  type?: string;
  placeholder?: string;
  error?: string;
  register: UseFormRegister<SignUpInput | SignInInput>; // React Hook Form register function
  disabled?: boolean;
}

const FormField = ({ id, label, type = 'text', placeholder, error, register, disabled }: FormFieldProps) => {
  return (
    <div className="mb-4">
      <Label htmlFor={id as string} className="text-white/90 mb-1 block">
        {label}
      </Label>
      <Input
        id={id as string}
        type={type}
        placeholder={placeholder}
        disabled={disabled}
        className={`w-full p-3 rounded-lg glass-card ${
          error ? 'border-red-500' : 'border-white/20'
        } ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
        {...register(id)}
      />
      {error && (
        <motion.p
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0 }}
          className="mt-1 text-sm text-red-400"
        >
          {error}
        </motion.p>
      )}
    </div>
  );
};

FormField.displayName = 'FormField';

export default FormField;