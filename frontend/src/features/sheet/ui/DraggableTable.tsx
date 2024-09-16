"use client";
import { useState, useReducer, useMemo, useEffect } from "react";
import Image from "next/image";
import {
  createColumnHelper,
  ColumnDef,
  getCoreRowModel,
  useReactTable,
} from "@tanstack/react-table";
import { stockAssets, Asset } from "@/features/sheet/model/types";
import DraggableTableHeader from "@/widgets/draggable-table/DraggableTableHeader";
import DragAlongCell from "./DragAlongCell";
import CustomColumnSelector from "@/features/sheet/ui/CustomColumnSelector";
import { Button } from "@/shared/ui/button/Button";
import { getDummyStockAssets } from "@/features/sheet/api";

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
import { CSSProperties } from "react";

const DraggableTable = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);

  const openModal = () => {
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
  };

  const columns = useMemo<ColumnDef<Asset>[]>(
    () => [
      {
        accessorKey: "stock_name",
        header: () => <span className="self-end">종목명</span>,
        id: "stock_name",
        size: 240,
      },
      {
        accessorKey: "quantity",
        header: "수량",
        id: "quantity",
        size: 240,
      },
      {
        accessorKey: "buy_date",
        header: "구매일자",
        id: "buy_date",
        size: 240,
      },
      {
        accessorKey: "investment_bank",
        header: "증권사",
        id: "investment_bank",
        size: 240,
      },
      {
        accessorKey: "account_type",
        header: "계좌종류",
        id: "account_type",
        size: 240,
      },
      {
        accessorKey: "profit_rate",
        header: "수익률",
        id: "profit_rate",
        size: 240,
      },
      {
        accessorKey: "opening_price",
        header: "시가",
        id: "opening_price",
        size: 240,
      },
      {
        accessorKey: "highest_price",
        header: "고가",
        id: "highest_price",
        size: 240,
      },
      {
        accessorKey: "lowest_price",
        header: "저가",
        id: "lowest_price",
        size: 240,
      },
      {
        accessorKey: "+",
        id: "+",
        header: () => (
          <div className="flex items-center">
            <Button
              variant="icon"
              size="icon"
              leftIcon={
                <Image
                  src="/images/add.svg"
                  alt="col custom button"
                  width={42}
                  height={42}
                />
              }
              onClick={openModal}
            ></Button>
          </div>
        ),
        cell: ({ getValue }) => (
          <Button
            variant="icon"
            size="icon"
            leftIcon={
              <Image
                src="/images/delete_row.svg"
                alt="delete button"
                width={32}
                height={32}
              />
            }
            onClick={() => alert("행 삭제")}
          ></Button>
        ),
      },
    ],
    [],
  );

  // const [data, setData] = useState(() => [...stockAssets]);
  //const rerender = useReducer(() => ({}), {})[1];
  // const rerender = () => setData(stockAssets);

  const [data, setData] = useState([]); // 데이터를 상태로 관리
  const [columnOrder, setColumnOrder] = useState<string[]>(() =>
    columns.map((c) => c.id!),
  );

    // 현재 columnOrder에 포함된 열만 필터링하여 렌더링
  const filteredColumns = useMemo(() => {
    return columns.filter((col) => columnOrder.includes(col.id!));
  }, [columns, columnOrder]);

  // API에서 데이터 불러오기
  const fetchData = async () => {
    try {
      const stockAssets = await getDummyStockAssets(); // API 호출
      setData(stockAssets); // 가져온 데이터를 상태로 설정
    } catch (error) {
      console.error("데이터를 불러오는 중 오류 발생:", error);
    }
  };

  // 컴포넌트가 처음 렌더링될 때 데이터를 불러옴
  useEffect(() => {
    fetchData();
  }, []);

  const table = useReactTable({
    data,
    columns: filteredColumns,
    getCoreRowModel: getCoreRowModel(),
    state: {
      columnOrder,
    },
    onColumnOrderChange: setColumnOrder,
    debugTable: true,
    debugHeaders: true,
    debugColumns: true,
  });

  // reorder columns after drag & drop
  function handleDragEnd(event: DragEndEvent) {
    const { active, over } = event;
    // 마지막 열의 id를 제외하고 드래그가 가능하게 제한
    const lastColumnId = columnOrder[columnOrder.length - 1];

    if (
      active &&
      over &&
      active.id !== over.id &&
      active.id !== lastColumnId &&
      over.id !== lastColumnId
    ) {
      setColumnOrder((columnOrder) => {
        const oldIndex = columnOrder.indexOf(active.id as string);
        const newIndex = columnOrder.indexOf(over.id as string);
        return arrayMove(columnOrder, oldIndex, newIndex); //this is just a splice util
      });
    }
  }

  const sensors = useSensors(
    useSensor(MouseSensor, {}),
    useSensor(TouchSensor, {}),
    useSensor(KeyboardSensor, {}),
  );

  return (
    // NOTE: This provider creates div elements, so don't nest inside of <table> elements
    <DndContext
      collisionDetection={closestCenter}
      modifiers={[restrictToHorizontalAxis]}
      onDragEnd={handleDragEnd}
      sensors={sensors}
    >
      <div className="relative mt-4 inline-block rounded-md border border-gray-30 bg-white">
        {isModalOpen && (
          <CustomColumnSelector
            onClose={closeModal}
            columnOrder={columnOrder}
            setColumnOrder={setColumnOrder}
          />
        )}
        <table className="border-collapse">
          <thead>
            {table.getHeaderGroups().map((headerGroup) => (
              <tr key={headerGroup.id}>
                <SortableContext
                  items={columnOrder.slice(0, -1)}
                  strategy={horizontalListSortingStrategy}
                >
                  {headerGroup.headers.map((header, index) => (
                    <DraggableTableHeader
                      key={header.id}
                      header={header}
                      isLastColumn={index === headerGroup.headers.length - 1}
                      isFixed={header.id === "+"}
                    />
                  ))}
                </SortableContext>
              </tr>
            ))}
          </thead>
          <tbody>
            {table.getRowModel().rows.map((row, rowIndex) => (
              <tr key={row.id}>
                {row.getVisibleCells().map((cell, index) => (
                  <DragAlongCell
                    key={cell.id}
                    cell={cell}
                    isLastColumn={index === row.getVisibleCells().length - 1}
                    isLastRow={rowIndex === table.getRowModel().rows.length - 1}
                  />
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </DndContext>
  );
};

export default DraggableTable;
