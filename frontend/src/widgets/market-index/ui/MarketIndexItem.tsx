import { IncDecRate } from "@/shared";

export default function MarketIndexItem({
  stockMarket,
  stockIndex,
  rate,
}: {
  stockMarket: string;
  stockIndex: number;
  rate: number;
}) {
  return (
    <div className="except-mobile:border-r-0 except-mobile:items-center except-mobile:space-x-[24px] flex shrink-0 justify-center border-r border-gray-20 px-[16px] text-heading-4 mobile:flex-col mobile:space-y-[12px]">
      <p>{stockMarket}</p>
      <div className="flex items-center space-x-[8px]">
        <p>{stockIndex}</p>
        <IncDecRate rate={rate} />
      </div>
    </div>
  );
}
