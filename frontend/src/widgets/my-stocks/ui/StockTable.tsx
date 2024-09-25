import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

export default function StockTable({ stocks }: { stocks: any[] }) {
  const blackSpace = (6 - stocks.length) * 48;
  return (
    <>
      <Table className="min-w-[612px] text-body-2">
        <TableHeader>
          <TableRow className="border-gray-20">
            <TableHead className="w-[160px]">종목명</TableHead>
            <TableHead className="w-[151px] text-right">현재가</TableHead>
            <TableHead className="w-[120px] text-right">수익률</TableHead>
            <TableHead className="w-[151px] text-right">수익금</TableHead>
            <TableHead className="w-[90px] text-right">수량</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {stocks.map((stock, i) => (
            <TableRow key={i} className="border-none">
              <TableCell className="w-[160px]">{stock.name}</TableCell>

              <TableCell className="w-[120px] text-right">
                ₩{stock.currentPrice.toLocaleString("ko-KR")}
              </TableCell>
              <TableCell
                className={`w-[151px] text-right ${stock.profitRate < 0 && "text-decrease"} ${stock.profitRate > 0 && "text-alert"}`}
              >
                {stock.profitRate > 0 && "+"}
                {stock.profitRate}%
              </TableCell>
              <TableCell className="w-[151px] text-right">
                ₩{stock.profitAmount.toLocaleString("ko-KR")}
              </TableCell>
              <TableCell className="w-[90px] text-right">
                {stock.quantity.toLocaleString()}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      {stocks.length < 6 && (
        <div
          className={`h-[1px] w-full bg-gray-20`}
          style={{ marginBottom: `${blackSpace}px` }}
        />
      )}
    </>
  );
}
