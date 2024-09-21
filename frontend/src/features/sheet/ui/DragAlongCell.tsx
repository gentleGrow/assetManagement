import React, { CSSProperties } from "react";
import { useState, useRef, useEffect } from "react";
import { Cell, flexRender } from "@tanstack/react-table";
import { useSortable } from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";

import StockCell from "@/features/sheet/ui/StockCell";
import BankCell from "@/features/sheet/ui/BankCell";
import AccountTypeCell from "@/features/sheet/ui/AccountTypeCell";

// needed for table body level scope DnD setup
import {
  DndContext,
  KeyboardSensor,
  MouseSensor,
  TouchSensor,
  closestCenter,
  type DragEndEvent,
  useSensor,
  useSensors,
} from "@dnd-kit/core";
import { restrictToHorizontalAxis } from "@dnd-kit/modifiers";
import {
  arrayMove,
  SortableContext,
  horizontalListSortingStrategy,
} from "@dnd-kit/sortable";

// needed for row & cell level scope DnD setup
import { useSortable } from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";

type DragAlongCellProps<T> = {
  cell: Cell<T, unknown>;
  isLastColumn: boolean;
  isLastRow: boolean;
  options?: any;
};

const DragAlongCell = <T,>({
  cell,
  isLastColumn,
  isLastRow,
  options,
}: DragAlongCellProps<T>) => {
  const { isDragging, setNodeRef, transform } = useSortable({
    id: cell.column.id,
  });
  const [isEditing, setIsEditing] = useState(false);
  const cellRef = useRef<HTMLDivElement | null>(null);
  const [cellValue, setCellValue] = useState<any>(cell.getValue() ?? "");

  useEffect(() => {
    setCellValue(cell.getValue()); // 셀의 초기값 설정
  }, [cell]);

  const style: CSSProperties = {
    opacity: isDragging ? 0.8 : 1,
    position: "relative",
    transform: CSS.Translate.toString(transform), // translate instead of transform to avoid squishing
    transition: "width transform 0.2s ease-in-out",
    width: cell.column.getSize(),
    zIndex: isDragging ? 1 : isEditing ? 1 : 0,
  };

  const onChange = (value) => {
    setCellValue(value);
  };
  
  const renderTableCell = () => {
    const cellType = cell.column.id;
    switch (cellType) {
      case "stock_name":
        return (
          <StockCell
            value={cellValue}
            code={cell.getContext().row.original?.["stock_code"]}
            onChange={onChange}
          />
        );
      case "investment_bank":
        return (
          <BankCell
            value={cellValue}
            onChange={onChange}
            bankList={options?.bankList}
          />
        );
      case "account_type":
        return (
          <AccountTypeCell
            value={cellValue}
            onChange={onChange}
            accountList={options?.accountList}
          />
        );
      default:
        return defaultCell();
    }
  };

  const defaultCell = () => {
    return (
      <div>{flexRender(cell.column.columnDef.cell, cell.getContext())}</div>
    );
  };

  // Handle click to enable editing mode
  const handleCellClick = () => {
    setIsEditing(true);
  };

  // Handle blur to disable editing mode
  const handleCellBlur = (e: React.FocusEvent) => {
    const relatedTarget = e.relatedTarget as HTMLElement | null;

    if (
      cellRef.current &&
      relatedTarget &&
      !cellRef.current.contains(e.relatedTarget)
    ) {
      setIsEditing(false);
    }
  };

  return (
    <td
      style={style}
      ref={setNodeRef}
      className={`border-gray-10 text-sm font-normal text-gray-90 ${
        isLastColumn ? "" : "border-r"
      } ${isLastRow ? "" : "border-b"} ${isEditing ? "z-100" : ""}`}
      onClick={handleCellClick}
      onBlur={handleCellBlur}
      tabIndex={0}
    >
      <div ref={cellRef} className="w-full px-1.5 py-2.5">
        {renderTableCell()}
      </div>
    </td>
  );
};

export default DragAlongCell;
