"use client";

import Input from "@/shared/ui/Input";
import { useState } from "react";

export default function ProfitCell({
  value,
  onChange,
}: {
  value?: any;
  onChange?: (value: any) => void;
}) {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { value } = e.target;
    if (onChange) {
      onChange(value);
    }
  };
  return (
    <>
      {value && (
        <div
          className={`py-\[9\.5px\] relative h-full w-full border-y text-right text-body-sm ${value === 0 ? "border-gray-10 bg-white text-gray-90" : value > 0 ? "text-alet border-[#FFECEC] bg-[#FFECEC]" : "border-[#DCEAFF] bg-[#DCEAFF] text-[#0A6CFF]"}`}
        >
          {value}%
        </div>
      )}
      {!value && (
        <div
          className={`py-\[9\.5px\] relative h-full w-full border-y border-gray-10 bg-gray-10 text-right text-body-sm text-gray-50`}
        >
          자동 계산 필드입니다.
        </div>
      )}
    </>
  );
}
