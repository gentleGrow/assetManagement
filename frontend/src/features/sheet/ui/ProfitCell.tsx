"use client";

import Input from "@/shared/ui/Input";
import { useState } from "react";

export default function ProfitCell({
  value,
  onChange,
  isNew,
}: {
  value?: any;
  onChange?: (value: any) => void;
  isNew?: boolean;
}) {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { value } = e.target;
    if (onChange) {
      onChange(value);
    }
  };

  const displayValue = () => {
    if (value) {
      const roundedValue = Math.round(value * 100) / 100;
      return `${roundedValue}`;
    }

    return value;
  };

  return (
    <>
      {isNew ? (
        <div
          className={`relative h-full w-full border-y border-gray-10 bg-gray-10 py-[9.5px] text-right text-body-sm text-gray-50`}
        >
          자동 계산 필드입니다.
        </div>
      ) : (
        <div
          className={`relative h-full w-full border-y py-[9.5px] text-right text-body-sm ${value === 0 ? "border-gray-10 bg-white text-gray-90" : value > 0 ? "text-alet border-[#FFECEC] bg-[#FFECEC]" : "border-[#DCEAFF] bg-[#DCEAFF] text-[#0A6CFF]"}`}
        >
          {displayValue()}%
        </div>
      )}
    </>
  );
}
