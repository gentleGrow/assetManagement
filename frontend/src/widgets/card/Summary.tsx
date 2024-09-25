import SummaryCard from "./SummaryCard";

interface SummaryProps {
  summaryData: {
    title: string;
    type: string;
    amount?: number;
  }[];
}

export default function Summary({ summaryData }: SummaryProps) {
  return (
    <div className="flex space-x-[16px]">
      {summaryData.map(({ title, type, amount }) => (
        <SummaryCard key={title} title={title} type={type} amount={amount} />
      ))}
    </div>
  );
}
