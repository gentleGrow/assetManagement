export default function PercentWithTitle({
  title,
  percent,
}: {
  title: string;
  percent: number;
}) {
  return (
    <div className="flex w-[131px] shrink-0 flex-col py-[8px] mobile:w-1/2">
      <p className="text-body-3 text-gray-70">{title}</p>
      <p className="text-[28px] font-bold leading-[33.61px]">{percent}%</p>
    </div>
  );
}
