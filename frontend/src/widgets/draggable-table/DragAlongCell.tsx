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

type DragAlongCellProps<T> = {
  cell: Cell<T, unknown>;
  isLastColumn: boolean;
  isLastRow: boolean;
};

const DragAlongCell = <T,>({
  cell,
  isLastColumn,
  isLastRow,
}: DragAlongCellProps<T>) => {
  const { isDragging, setNodeRef, transform } = useSortable({
    id: cell.column.id,
  });

  const style: CSSProperties = {
    opacity: isDragging ? 0.8 : 1,
    position: "relative",
    transform: CSS.Translate.toString(transform), // translate instead of transform to avoid squishing
    transition: "width transform 0.2s ease-in-out",
    width: cell.column.getSize(),
    zIndex: isDragging ? 1 : 0,
  };

  return (
    <td
      style={style}
      ref={setNodeRef}
      className={`border-gray-10 text-sm font-normal text-gray-90 ${
        isLastColumn ? "" : "border-r"
      } ${isLastRow ? "" : "border-b"}`}
    >
      <div className="w-full px-1.5 py-2.5">
        {flexRender(cell.column.columnDef.cell, cell.getContext())}
      </div>
    </td>
  );
};

export default DragAlongCell;
