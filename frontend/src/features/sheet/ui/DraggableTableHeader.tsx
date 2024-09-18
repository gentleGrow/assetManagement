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
    <div className="w-full px-1.5 py-2.5 text-left">
      {header.isPlaceholder
        ? null
        : flexRender(header.column.columnDef.header, header.getContext())}
    </div>
  );

  return (
    <th
      key={header.id}
      colSpan={header.colSpan}
      ref={setNodeRef}
      style={style}
      className={`border-b border-gray-30 text-sm font-semibold text-gray-100 ${
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
              className="absolute right-0 top-0 flex h-full items-center justify-center"
              onClick={header.column.getToggleSortingHandler()}
            >
              <span
                className={`absolute ml-2 transition-opacity duration-200 ${header.column.getIsSorted() ? "opacity-100" : "opacity-0 group-hover:opacity-0"}`}
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
