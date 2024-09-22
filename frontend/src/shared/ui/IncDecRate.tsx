export default function IncDecRate({
  rate,
  className = "",
}: {
  rate: number;
  className?: string;
}) {
  return (
    <div
      aria-label={`The rate is ${rate > 0 ? "increased" : rate < 0 ? "decreased" : "unchanged"} by ${rate}%`}
      className={`flex h-[24px] w-[64px] items-center justify-center rounded-md px-[8px] py-[3px] text-body-4 ${rate === 0 ? "bg-gray-5 text-gray-50" : rate > 0 ? "bg-alert/10 text-alert" : "bg-decrease/10 text-decrease"} ${className}`}
    >
      {rate > 0 && "+"}
      {rate}%
    </div>
  );
}
