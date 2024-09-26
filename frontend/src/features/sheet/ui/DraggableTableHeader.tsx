import React, { CSSProperties } from "react";
import Image from "next/image";

import { Header, flexRender } from "@tanstack/react-table";

// needed for row & cell level scope DnD setup
import { useSortable } from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";

type DraggableTableHeaderProps<T> = {
  header: Header<T, unknown>;
  isLastColumn: boolean;
  isTextLeft?: boolean;
  isFixed?: boolean;
};

const DraggableTableHeader = <T,>({
  header,
  isLastColumn,
  isFixed,
}: DraggableTableHeaderProps<T>) => {
  const { attributes, isDragging, listeners, setNodeRef, transform } =
    useSortable({
      id: header.column.id,
    });

  const style: CSSProperties = {
    opacity: isDragging ? 0.8 : 1,
    position: "relative",
    transform: CSS.Translate.toString(transform), // translate instead of transform to avoid squishing
    transition: "width transform 0.2s ease-in-out",
    whiteSpace: "nowrap",
    width: header.column.getSize(),
    zIndex: isDragging ? 1 : 0,
  };

  const sortIcon = {
    asc: (
      <Image
        src="/images/sorting_up_hover.svg"
        alt="sorting"
        width={20}
        height={20}
      />
    ),
    desc: (
      <Image
        src="/images/sorting_down_hover.svg"
        alt="sorting"
        width={20}
        height={20}
      />
    ),
  }[(header.column.getIsSorted() as string) ?? "null"];

  const selectedSortIcon = {
    asc: (
      <Image
        src="/images/sorting_up_selected.svg"
        alt="sorting"
        width={20}
        height={20}
      />
    ),
    desc: (
      <Image
        src="/images/sorting_down_selected.svg"
        alt="sorting"
        width={20}
        height={20}
      />
    ),
  }[(header.column.getIsSorted() as string) ?? "null"];

  const HeaderContent = () => (
    <div
      className={`w-full px-[10px] py-[12.5px] text-left ${isLeft() ? "text-left" : "text-right group-hover:pr-[24px]"} ${header.column.getIsSorted() && !isLeft() ? "pr-[24px]" : ""}`}
    >
      {header.isPlaceholder
        ? null
        : flexRender(header.column.columnDef.header, header.getContext())}
      {isRequired() && (
        <span className="pl-[3px] text-left text-green-60">*</span>
      )}
    </div>
  );

  const isLeft = () => {
    if (
      header.id === "stock_name" ||
      header.id === "buy_date" ||
      header.id === "investment_bank" ||
      header.id === "account_type" ||
      header.id === "+"
    ) {
      return true;
    }
    return false;
  };

  const isRequired = () => {
    if (
      header.id === "stock_name" ||
      header.id === "quantity" ||
      header.id === "buy_date"
    ) {
      return true;
    }
    return false;
  };

  return (
    <th
      key={header.id}
      colSpan={header.colSpan}
      ref={setNodeRef}
      style={style}
      className={`border-gray-30 p-0 text-[14px] font-semibold leading-[17px] text-gray-100 ${
        isLastColumn ? "" : "border-r"
      } group`}
    >
      {isFixed ? (
        <HeaderContent />
      ) : (
        <div className="relative w-full">
          <button className="w-full" {...attributes} {...listeners}>
            <HeaderContent />
          </button>
          {header.column.getCanSort() && (
            <button
              className={`absolute ${isLeft() ? "left-[60px] top-0" : "right-0 top-0"} flex h-full items-center justify-center`}
              onClick={header.column.getToggleSortingHandler()}
            >
              <span
                className={`absolute ml-2 transition-opacity duration-200 group-hover:opacity-0 ${header.column.getIsSorted() ? "opacity-100" : "opacity-0 group-hover:opacity-0"}`}
              >
                {selectedSortIcon}
              </span>
              <span className="z-1 ml-2 opacity-0 transition-opacity duration-200 group-hover:opacity-100">
                {sortIcon ?? (
                  <Image
                    src="/images/sorting_down_hover.svg"
                    alt="sorting"
                    width={20}
                    height={20}
                  />
                )}
              </span>
            </button>
          )}
        </div>
      )}
    </th>
  );
};

export default DraggableTableHeader;
