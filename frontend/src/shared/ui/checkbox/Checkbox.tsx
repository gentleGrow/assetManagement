// CustomCheckbox.tsx
import React from "react";

interface Checkbox {
  label: string;
  checked: boolean;
  required: boolean;
  onChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
}

const Checkbox: React.FC<Checkbox> = ({
  label,
  checked,
  required,
  onChange,
}) => {
  return (
    <label className="flex flex-1 cursor-pointer items-center space-x-1.5">
      <input
        type="checkbox"
        className="hidden"
        checked={checked}
        onChange={onChange}
        disabled={required}
      />
      <div
        className={`flex h-4 w-4 items-center justify-center rounded-[2px] border ${checked ? "border-transparent bg-green-60" : "border-gray-30"} ${required ? "opacity-40" : null}`}
      >
        {checked && (
          <svg
            className="h-4 w-4 text-white"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path strokeWidth="3" d="M4 12l5 5L20 6"></path>
          </svg>
        )}
      </div>
      {label && (
        <span
          className={`text-sm font-normal ${required ? "text-gray-40" : "text-gray-60"}`}
        >
          {label}
        </span>
      )}
    </label>
  );
};

export default Checkbox;
