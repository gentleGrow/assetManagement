"use client";

import { useRef, useEffect, useState } from "react";
import Image from "next/image";
import SortableList from "@/widgets/sortable-list/ui/SortableList";
import { Button } from "@/shared/ui/button/Button";

interface Column {
  id: string;
  label: string;
  required: boolean;
  checked: boolean;
}

interface CustomColumnSelectorProps {
  onClose: () => void;
  columnOrder: string[];
  setColumnOrder: (columnOrder: string[]) => void;
}

const columns: Column[] = [
  { id: "stock_name", label: "종목명", required: true, checked: true },
  { id: "quantity", label: "수량", required: true, checked: true },
  { id: "purchase_amount", label: "매입금액", required: true, checked: true },
  { id: "buy_date", label: "구매일자", required: true, checked: true },
  { id: "investment_bank", label: "증권사", required: false, checked: true },
  { id: "account_type", label: "계좌 종류", required: false, checked: true },
  { id: "profit_rate", label: "수익률", required: false, checked: true },
  { id: "profit_amount", label: "수익금", required: false, checked: true },
  { id: "purchase_price", label: "매입가", required: false, checked: false },
  { id: "current_price", label: "현재가", required: false, checked: true },
  { id: "opening_price", label: "시가", required: false, checked: true },
  { id: "highest_price", label: "고가", required: false, checked: true },
  { id: "lowest_price", label: "저가", required: false, checked: false },
  { id: "dividend", label: "배당금", required: false, checked: false },
];
// purchase_currency_type 매입 통화
// id
// stock_code 종목명
// stock_volume 주식 하루 중 거래량

const CustomColumnSelector: React.FC<CustomColumnSelectorProps> = ({
  onClose,
  columnOrder,
  setColumnOrder,
}) => {
  const [filteredColumns, setFilteredColumns] = useState<Column[]>([]);

  useEffect(() => {
    const orderedColumns = columnOrder
      .map((id) => {
        const column = columns.find((col) => col.id === id);
        if (column) {
          return { ...column, checked: true };
        }
        return null;
      })
      .filter(Boolean) as Column[]; // null 값을 제거하고 타입 단언

    const remainingColumns = columns
      .filter((col) => !columnOrder.includes(col.id))
      .map((col) => ({ ...col, checked: false }));

    const newColumns = [...orderedColumns, ...remainingColumns];
    setFilteredColumns(newColumns);
  }, [columnOrder]);

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

  const handleApply = () => {
    const selectedColumns: string[] = filteredColumns.reduce(
      (acc: string[], column) => {
        if (column.checked) {
          acc.push(column.id);
        }
        return acc;
      },
      [],
    );

    setColumnOrder([...selectedColumns, "+"]);
    onClose();
  };

  return (
    <div className="absolute right-0 top-12 z-50 flex h-[400px] w-[204px] flex-col space-y-2 rounded rounded-lg border border-gray-20 bg-white p-[10px] shadow-xl">
      <div className="flex justify-between border-b pb-[5px]">
        <Button
          variant="icon"
          size="xs"
          leftIcon={
            <Image
              src="/images/refresh.svg"
              alt="refresh button"
              width={16}
              height={16}
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
            <Image
              src="/images/close.svg"
              alt="close button"
              width={20}
              height={20}
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
      <SortableList
        filteredColumns={filteredColumns}
        setFilteredColumns={setFilteredColumns}
      />
      <Button variant="primary" size="md" onClick={handleApply}>
        적용하기
      </Button>
    </div>
  );
};

export default CustomColumnSelector;
