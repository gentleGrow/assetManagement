import { ColumnDef, SortingFn } from "@tanstack/react-table";
import { Asset } from "@/features/sheet/model/types";
import { Button } from "@/shared/ui/button/Button";
import Image from "next/image";

export const useTableColumns = (openModal: () => void): ColumnDef<Asset>[] => {
  const dateSorting: SortingFn<any> = (rowA, rowB, columnId) => {
    const dateA = new Date(rowA.getValue(columnId)).getTime();
    const dateB = new Date(rowB.getValue(columnId)).getTime();

    if (dateA > dateB) return 1;
    if (dateA < dateB) return -1;
    return 0;
  };

  return [
    {
      accessorKey: "stock_name",
      header: () => <span className="self-end">종목명</span>,
      id: "stock_name",
      size: 240,
      enableSorting: true,
    },
    {
      accessorKey: "quantity",
      header: "수량",
      id: "quantity",
      size: 240,
      enableSorting: true,
    },
    {
      accessorKey: "buy_date",
      header: "구매일자",
      id: "buy_date",
      size: 240,
      enableSorting: true,
      sortingFn: dateSorting,
    },
    {
      accessorKey: "investment_bank",
      header: "증권사",
      id: "investment_bank",
      size: 240,
      enableSorting: true,
    },
    {
      accessorKey: "account_type",
      header: "계좌종류",
      id: "account_type",
      size: 240,
      enableSorting: true,
    },
    {
      accessorKey: "profit_rate",
      header: "수익률",
      id: "profit_rate",
      size: 240,
      enableSorting: true,
    },
    {
      accessorKey: "opening_price",
      header: "시가",
      id: "opening_price",
      size: 240,
      enableSorting: true,
    },
    {
      accessorKey: "highest_price",
      header: "고가",
      id: "highest_price",
      size: 240,
      enableSorting: true,
    },
    {
      accessorKey: "lowest_price",
      header: "저가",
      id: "lowest_price",
      size: 240,
      enableSorting: true,
    },
    {
      accessorKey: "+",
      id: "+",
      enableSorting: false,
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
  ];
};
