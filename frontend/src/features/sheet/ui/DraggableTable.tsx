"use client";
import { useState, useReducer, useMemo, useEffect } from "react";
import Image from "next/image";
import {
  getCoreRowModel,
  useReactTable,
  getSortedRowModel,
} from "@tanstack/react-table";
import DraggableTableHeader from "./DraggableTableHeader";
import DragAlongCell from "./DragAlongCell";
import { useTableColumns } from "./TableColumns";

import CustomColumnSelector from "@/features/sheet/ui/CustomColumnSelector";
import { Button } from "@/shared/ui/button/Button";
import { getDummyStockAssets } from "@/features/sheet/api";

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
import { getAllStocks, getAllOptions } from "@/features/sheet/api";
import { saveStocks } from "@/shared/lib/indexedDB";

const DraggableTable = ({ tableData, setTableData }) => {
  const [isModalOpen, setIsModalOpen] = useState(false);

  const openModal = () => {
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
  };

  const columns = useTableColumns(openModal);

  const [columnOrder, setColumnOrder] = useState<string[]>(() =>
    columns.map((c) => c.id!),
  );

  // 현재 columnOrder에 포함된 열만 필터링하여 렌더링
  const filteredColumns = useMemo(() => {
    return columns.filter((col) => columnOrder.includes(col.id!));
  }, [columns, columnOrder]);

  const [stockList, setStockList] = useState<any[]>([]); // 데이터를 상태로 관리

  const fetchComboOptions = async () => {
    try {
      const stockList = await getAllStocks(); // API 호출
      setStockList(stockList); // 가져온 데이터를 상태로 설정
      saveStocks(stockList);
    } catch (error) {
      console.error("데이터를 불러오는 중 오류 발생:", error);
    }
  };

  const [options, setOptions] = useState<{
    bankList: { id: any; name: any }[];
    accountList: { id: any; name: any }[];
  }>({ bankList: [], accountList: [] });

  const fetchOptions = async () => {
    try {
      const options = await getAllOptions();
      setOptions({
        bankList: options.bankList,
        accountList: options.accountList,
      });
    } catch (error) {
      console.error("데이터를 불러오는 중 오류 발생:", error);
    }
  };

  useEffect(() => {
    fetchComboOptions();
    fetchOptions();
  }, []);

  const [sorting, setSorting] = useState<any[]>([]);

  const table = useReactTable({
    data: tableData,
    columns: filteredColumns,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(), // 정렬을 위한 RowModel 추가
    state: {
      columnOrder,
      sorting, // 현재 정렬 상태 반영
    },
    onColumnOrderChange: setColumnOrder,
    onSortingChange: setSorting,
    enableSortingRemoval: false,
    enableMultiSort: false,
  });

  function handleDragEnd(event: DragEndEvent) {
    const { active, over } = event;
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

  const addRow = () => {
    const newRow = {
      id: Date.now(), // 임시 ID 생성, 서버에서 응답받을 실제 ID로 대체 가능
      stock_name: "",
      quantity: 0,
      buy_date: "",
      investment_bank: "",
      account_type: "",
      profit_rate: 0,
      opening_price: 0,
      highest_price: 0,
      lowest_price: 0,
      isNew: true, // 새로 추가된 행임을 나타내는 플래그
    };

    setData((prevData) => [...prevData, newRow]);
  };

  return (
    <DndContext
      collisionDetection={closestCenter}
      modifiers={[restrictToHorizontalAxis]}
      onDragEnd={handleDragEnd}
      sensors={sensors}
    >
      <div className="w-full overflow-auto relative mt-4 inline-block rounded-md border border-gray-30 bg-white">
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
                    options={options}
                  />
                ))}
              </tr>
            ))}
            <tr>
              <td colSpan={filteredColumns.length}>
                <Button
                  variant="icon"
                  size="xs"
                  leftIcon={
                    <Image
                      src="/images/add_row.svg"
                      alt="add row button"
                      width={24}
                      height={24}
                    />
                  }
                  style={{ color: "var(--gray-100)" }}
                  onClick={addRow}
                >
                  행 추가
                </Button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </DndContext>
  );
};

export default DraggableTable;
