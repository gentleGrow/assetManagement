"use client";

import Input from "@/shared/ui/Input";
import { useState } from "react";
import Image from "next/image";

export default function NumberCell({
  value,
  onChange,
}: {
  value?: any;
  onChange?: (value: any) => void;
}) {
  const [isError, setIsError] = useState(false);
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { value } = e.target;
    if (/^\d*$/.test(value)) {
      if (onChange) {
        onChange(value);
        setIsError(false);
      }
    } else {
      setIsError(true);
    }
  };

  return (
    <div className="relative w-full">
      <Input
        type="text"
        value={value}
        onChange={handleChange}
        isError={isError}
      />
      {isError && (
        <div className="absolute left-0 top-[-24px] flex h-[24px] items-center justify-center rounded-[4px] bg-alert p-[4px]">
          <Image src="/images/error.svg" alt="error" width={16} height={16} />
          <span className="pl-[2px] text-[10px] leading-[12px] text-white">
            숫자만 입력할 수 있어요.
          </span>
        </div>
      )}
    </div>
  );
}
