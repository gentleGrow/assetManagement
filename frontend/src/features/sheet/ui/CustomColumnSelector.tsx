"use client";

import { useRef } from "react";
import SortableList from "@/widgets/sortable-list/ui/SortableList";
import { Button } from "@/shared/ui/button/Button";

const CustomColumnSelector = ({ onClose }) => {
  const columns = [
    { id: "1", label: "종목명", required: true, checked: true },
    { id: "2", label: "수량", required: true, checked: true },
    { id: "3", label: "구매일자", required: true, checked: true },
    { id: "4", label: "증권사", required: false, checked: true },
    { id: "5", label: "계좌 종류", required: false, checked: true },
    { id: "6", label: "수익률", required: false, checked: true },
    { id: "7", label: "매입가", required: false, checked: false },
    { id: "8", label: "배당금", required: false, checked: false },
    { id: "9", label: "시가", required: false, checked: true },
    { id: "10", label: "고가", required: false, checked: true },
    { id: "11", label: "저가", required: false, checked: false },
    { id: "12", label: "매입가", required: false, checked: false },
  ];

  const guidelines = [
    "*최대 10개까지 추가할 수 있습니다.",
    "*종목명, 수량, 구매일자는 필수 항목입니다.",
  ];

  const buttonRef = useRef<HTMLButtonElement>(null);

  const handleClick = () => {
    if (buttonRef.current) {
      console.log("Button clicked!", buttonRef.current);
    }
  };

  return (
    <div className="absolute right-0 top-12 z-50 flex h-[400px] w-[204px] flex-col space-y-2 rounded rounded-lg border border-gray-20 bg-white p-[10px] shadow-xl">
      <div className="flex justify-between border-b pb-[5px]">
        <Button
          variant="icon"
          size="xs"
          leftIcon={
            <img
              src="/images/refresh.svg"
              alt="refresh button"
              aria-hidden="true"
            />
          }
          style={{ color: "var(--gray-100)" }}
          onClick={() => alert("버튼 클릭!")}
        >
          초기화
        </Button>
        <Button
          variant="icon"
          size="icon"
          leftIcon={
            <img
              src="/images/close.svg"
              alt="close button"
              aria-hidden="true"
            />
          }
          onClick={() => onClose()}
        ></Button>
      </div>
      <div className="rounded bg-gray-5 p-2">
        {guidelines?.map((text: string) => (
          <p key={text} className="text-[11px] text-gray-70">
            {text}
          </p>
        ))}
      </div>
      <SortableList columns={columns} />
      <Button
        variant="primary"
        size="md"
        isLoading={false}
        onClick={() => alert("버튼 클릭!")}
        children="적용하기"
      ></Button>
    </div>
  );
};

export default CustomColumnSelector;
