"use client";
import InputWithImage from "@/shared/ui/InputWithInput";
import { useState } from "react";

export default function SearchBar() {
  const [value, setValue] = useState<string>("");
  return (
    <InputWithImage
      props={{
        type: "text",
        placeholder: "종목명을 입력해주세요.",
        value: value,
        onChange: (e) => setValue(e.target.value),
        classNames: "min-w-[491px] h-[36px]",
      }}
    >
      <svg
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <rect width="24" height="24" fill="white" />
        <path
          d="M16 16L19 19"
          stroke="#5D646E"
          strokeWidth="1.5"
          strokeLinecap="round"
        />
        <circle
          cx="11.5"
          cy="11.5"
          r="5.75"
          stroke="#5D646E"
          strokeWidth="1.5"
        />
      </svg>
    </InputWithImage>
  );
}
