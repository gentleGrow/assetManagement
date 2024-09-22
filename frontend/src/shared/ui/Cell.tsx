import React from "react";
import clsx from "clsx";

export interface InputProps {
  type: string;
  classNames?: string;
  placeholder?: string;
  value?: string;
  withImage?: boolean;
  onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void;
  isHovered?: boolean;
  isSelected?: boolean;
  isDisabled?: boolean;
  isDone?: boolean;
  isError?: boolean;
  isKRW?: boolean;
  children?: React.ReactNode;
}

export default function Cell({
  type,
  classNames,
  placeholder,
  value,
  withImage,
  onChange,
  isHovered = false,
  isSelected = false,
  isDisabled = false,
  isError = false,
  isKRW = true,
  children,
}: InputProps) {
  return (
    <div
      className={clsx(
        `font-regular flex w-full items-center justify-end rounded-md border border-gray-20 px-[10px] py-[9.5px] text-body-sm text-gray-100 focus-within:!border-green-60 hover:border-gray-40 focus:outline-none disabled:border-gray-20 disabled:bg-white disabled:text-gray-30`,
        classNames,
        {
          "pl-[44px]": withImage,
          "border-gray-20 bg-white text-gray-30": isDisabled,
          "border-green-60": isSelected && !isError,
          "border-gray-40": isHovered && !isError,
          "!border-alert": isError,
        },
      )}
    >
      {children}
      <input
        type={type}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        disabled={isDisabled}
        className={clsx(
          `text-right outline-none`, // 텍스트를 오른쪽 정렬
          {
            "border-none bg-transparent": true, // 테두리 없애고 투명 배경
          },
        )}
        style={{
          width: `${String(value)?.length}ch`, // 입력 내용 크기만큼 너비 설정
          minWidth: "2ch", // 최소 너비 설정
          maxWidth: "100%", // 최대 너비 설정
        }}
      />
    </div>
  );
}
