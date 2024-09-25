import SeeMoreButton from "./SeeMoreButton";
import StockTable from "./StockTable";
const stocks = [
  {
    name: "삼성전자",
    currentPrice: 86700,
    profitRate: 5.31,
    profitAmount: 48873,
    quantity: 10,
  },
  {
    name: "바이두",
    currentPrice: 21700,
    profitRate: 7.12,
    profitAmount: 3100,
    quantity: 1,
  },
  {
    name: "Apple",
    currentPrice: 17100,
    profitRate: 0,
    profitAmount: 10800,
    quantity: 2000,
  },
  {
    name: "에코프로",
    currentPrice: 12041,
    profitRate: -5.31,
    profitAmount: 1590,
    quantity: 3,
  },
];

export default function MyStocks() {
  return (
    <div className="rounded-xl border border-gray-20 mobile:border-none">
      <div className="flex items-center justify-between p-[16px]">
        <h3 className="text-heading-2">내 보유주식</h3>
        <SeeMoreButton href={"/"} />
      </div>
      <div className="border-t border-gray-20">
        {stocks.length === 0 ? (
          <div className="flex h-[288px] items-center justify-center">
            <p className="text-center text-body-2">
              표시할 데이터가 없어요.
              <br />
              <span className="text-green-60">시트</span>에서 투자 정보를 먼저
              입력해 주세요.
            </p>
          </div>
        ) : (
          <StockTable stocks={stocks} />
        )}
      </div>
    </div>
  );
}
