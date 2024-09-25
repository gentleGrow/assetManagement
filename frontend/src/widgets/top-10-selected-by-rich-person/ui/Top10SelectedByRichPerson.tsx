import { IncDecRate } from "@/shared";
import Image from "next/image";
import Top10SelectedByRichPersonItem from "./Top10SelectedByRichPersonItem";

const top10Stocks = [
  {
    rank: 1,
    name: "최대 글자수-width130",
    price: 111100000000,
    rate: 11.29,
  },
  { rank: 2, name: "SK하이닉스", price: 183200, rate: 11.2 },
  { rank: 3, name: "현대차", price: 27100, rate: 99.99 },
  { rank: 4, name: "카카오", price: 49500, rate: 99.99 },
  { rank: 5, name: "NAVER", price: 190100, rate: 99.99 },
  { rank: 6, name: "삼성SDI", price: 412000, rate: 0.0 },
  { rank: 7, name: "삼성전자", price: 156200, rate: -1.9 },
  { rank: 8, name: "기아", price: 108900, rate: -0.09 },
  { rank: 9, name: "LG전자", price: 95100, rate: -2.09 },
  { rank: 10, name: "현대모비스", price: 245500, rate: -39.99 },
];
export default function Top10SelectedByRichPerson() {
  return (
    <div className="space-y-[16px] rounded-lg border border-gray-20 p-[16px] mobile:rounded-none mobile:border-none">
      <div className="flex items-center space-x-[8px]">
        <h2 className="text-heading-2">부자들이 선택한 종목 TOP10</h2>
        <Image src={"/images/tip.svg"} width={16} height={16} alt="tip" />
      </div>
      <div>
        <ul>
          {top10Stocks.map((stock) => (
            <li key={stock.rank}>
              <Top10SelectedByRichPersonItem stock={stock} />
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
