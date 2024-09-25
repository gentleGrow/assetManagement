import React, { CSSProperties } from "react";
import ReactDOM from "react-dom/client";

import {
  Cell,
  ColumnDef,
  Header,
  flexRender,
  getCoreRowModel,
  useReactTable,
} from "@tanstack/react-table";

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

type DraggableTableHeaderProps<T> = {
  header: Header<T, unknown>;
  isLastColumn: boolean;
  isTextLeft?: boolean;
};

const DraggableTableHeader = <T,>({
  header,
  isLastColumn,
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

  return (
    <th
      colSpan={header.colSpan}
      ref={setNodeRef}
      style={style}
      className={`border-b border-gray-30 text-sm font-semibold text-gray-100 ${
        isLastColumn ? "" : "border-r"
      }`}
    >
      <button className={"w-full"} {...attributes} {...listeners}>
        <div className={`"text-left" w-full px-1.5 py-2.5`}>
          {header.isPlaceholder
            ? null
            : flexRender(header.column.columnDef.header, header.getContext())}
        </div>
      </button>
    </th>
  );
};

export default DraggableTableHeader;
