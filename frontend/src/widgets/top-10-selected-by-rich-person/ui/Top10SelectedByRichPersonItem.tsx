import { IncDecRate } from "@/shared";
import Image from "next/image";

interface Stock {
  rank: number;
  name: string;
  price: number;
  rate: number;
}

export default function Top10SelectedByRichPersonItem({
  stock,
}: {
  stock: Stock;
}) {
  return (
    <div className="flex h-[52px] items-center justify-between px-[4px]">
      <div className="flex space-x-[8px]">
        <p
          className={`${stock.rank < 4 && "text-green-60"} flex w-[2ch] items-center justify-center`}
        >
          {stock.rank}
        </p>
        <Image
          src="/images/stock_test_logo.svg"
          width={28}
          height={28}
          alt={stock.name}
        />
        <p className="text-body-2 flex items-center">{stock.name}</p>
      </div>

      <div className="flex space-x-[12px]">
        <p className="text-body-3 flex items-center">
          ₩{stock.price.toLocaleString("ko-KR")}
        </p>
        <IncDecRate rate={stock.rate} />
      </div>
    </div>
  );
}
