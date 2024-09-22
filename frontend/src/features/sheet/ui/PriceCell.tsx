"use client";

import Cell from "@/shared/ui/Cell";

export default function PriceCell({
  value,
  onChange,
  isEditable,
  isNew,
  isKRW,
}: {
  value?: any;
  onChange?: (value: any) => void;
  isEditable?: boolean;
  isNew?: boolean;
  isKRW?: boolean;
}) {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { value } = e.target;
    if (/^\d*$/.test(value)) {
      if (onChange) {
        onChange(value);
      }
    }
  };
  return (
    <>
      {isEditable && (
        <div className="relative">
          <div className="absolute top-1/2 -translate-y-1/2 pl-[10px]"></div>
          <Cell
            type="text"
            value={value}
            onChange={handleChange}
            isKRW={isKRW}
          >
      <span className="mr-[2px]">{isKRW ? "₩" : "$"}</span>

          </Cell>
        </div>
      )}
      {!isEditable && !isNew && value > 0 && (
        <div
          className={`py-\[9\.5px\] relative h-full w-full border-y text-right text-body-sm`}
        >
          <span className="mr-[2px]">{isKRW ? "₩" : "$"}</span>
          <span>{value}</span>
        </div>
      )}
      {!isEditable && !isNew && !value && (
        <div
          className={`py-\[9\.5px\] relative h-full w-full border-y border-gray-10 bg-gray-10 text-right text-body-sm text-gray-50`}
        >
          배당금이 없는 종목이에요.
        </div>
      )}
      {!isEditable && isNew && (
        <div
          className={`py-\[9\.5px\] relative h-full w-full border-y border-gray-10 bg-gray-10 text-right text-body-sm text-gray-50`}
        >
          자동 계산 필드입니다.
        </div>
      )}
    </>
  );
}
