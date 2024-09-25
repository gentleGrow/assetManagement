// components/PriceDisplay.js
export default function PriceDisplay({ price }) {
  const formattedNumber = new Intl.NumberFormat("ko-KR", {
    style: "currency",
    currency: "KRW",
  }).format(price);

  return <div className="text-xl font-semibold">{formattedNumber}</div>;
}
