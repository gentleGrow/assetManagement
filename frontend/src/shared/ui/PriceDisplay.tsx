// components/PriceDisplay.js
export default function PriceDisplay({ price }) {
  const formattedNumber = new Intl.NumberFormat("ko-KR", {
    style: "currency",
    currency: "KRW",
  }).format(price);

  return (
    <div className="w-auto overflow-hidden text-ellipsis whitespace-nowrap text-[24px] font-semibold leading-[29px]">
      {formattedNumber}
    </div>
  );
}
