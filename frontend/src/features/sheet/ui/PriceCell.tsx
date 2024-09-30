"use client";

import { useState } from "react";
import clsx from "clsx";

export default function PriceCell({
  value,
  onChange,
  isAutoCalc = false,
  isNew = false,
  isKRW = true,
  isDividend = false,
}: {
  value?: any;
  onChange?: (value: any) => void;
  isAutoCalc?: boolean;
  isNew?: boolean;
  isKRW?: boolean;
  isDividend?: boolean;
}) {
  const [internalValue, setInternalValue] = useState(value || "");
  const [isFocused, setIsFocused] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { value } = e.target;
    if (/^\d*$/.test(value)) {
      if (onChange) {
        onChange(value);
      }
    }
  };

  const handleFocus = () => {
    setIsFocused(true);
  };

  const handleBlur = () => {
    setIsFocused(false);
  };

  const renderAutoCalcCell = () => {
    return (
      <>
        {isNew ? (
          <div
            className={`relative h-full w-full truncate border-y border-gray-10 bg-gray-10 py-[9.5px] text-right text-body-sm text-gray-50`}
          >
            자동 계산 필드입니다.
          </div>
        ) : isDividend && !value ? (
          <div
            className={`relative h-full w-full truncate border-y border-gray-10 bg-gray-10 py-[9.5px] text-right text-body-sm text-gray-50`}
          >
            배당금이 없는 종목이에요.
          </div>
        ) : (
          renderInput(true)
        )}
      </>
    );
  };

  const renderInput = (isDisabled = false) => {

    const displayValue = () => {
      if (isDisabled && value) {
        // isDisabled가 true일 경우 value를 소수 둘째 자리까지 반올림
        const roundedValue = Math.round(value * 100) / 100;
        return `${isKRW ? "₩ " : "$ "}${roundedValue}`;
      }

      // 그 외의 경우는 기존 내부 값 표시
      return internalValue ? `${isKRW ? "₩ " : "$ "}${internalValue}` : "";
    };
    return (
      <div className={`relative`}>
        <div
          className={clsx(
            `font-regular flex w-full items-center justify-end rounded-md px-[10px] py-[9.5px] text-body-sm focus-within:!text-gray-90 ${value ? "text-gray-90" : "text-gray-50"} focus-within:ring-1 focus-within:ring-green-60 focus:outline-none disabled:border-gray-20 disabled:bg-white disabled:text-gray-30`,
          )}
        >
          {!internalValue && isFocused && (
            <span className={`"mr-[2px]" text-gray-90`}>
              {isKRW ? "₩" : "$"}
            </span>
          )}
          <input
            type={"text"}
            placeholder={isKRW ? "₩ 0" : "$ 0"}
            value={displayValue()}
            onChange={handleChange}
            disabled={isDisabled}
            className={clsx(
              `text-right outline-none focus:placeholder-transparent`, // 텍스트를 오른쪽 정렬
              {
                "border-none bg-transparent": true, // 테두리 없애고 투명 배경
              },
            )}
            // style={{
            //   width: `${value ? String(value)?.length : 1}ch`, // 입력 내용 크기만큼 너비 설정
            //   minWidth: "1ch", // 최소 너비 설정
            //   maxWidth: "100%", // 최대 너비 설정
            // }}
            onFocus={handleFocus}
            onBlur={handleBlur}
          />
        </div>
      </div>
    );
  };

  return (
    <>
      {isAutoCalc && renderAutoCalcCell()}
      {!isAutoCalc && renderInput()}
    </>
  );
}

// {!isAutoCalc && !isNew && value > 0 && (
//   <div
//     className={`relative h-full w-full border-y py-[9.5px] text-right text-body-sm`}
//   >
//     <span
//       className={`${value ? "text-gray-90" : "text-gray-50"} "mr-[2px]"`}
//     >
//       {isKRW ? "₩" : "$"}
//     </span>
//     <span>{value}</span>
//   </div>
// )}
