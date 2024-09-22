import Card from "@/shared/ui/Card";
import PriceDisplay from "@/shared/ui/PriceDisplay";
import { IncDecRate } from "@/shared";
interface SummaryCardProps {
  title?: string;
  type?: string;
  amount?: number;
  rate?: number;
}

export default function SummaryCard({ title, amount, rate }: SummaryCardProps) {
  return (
    <div className="min-w-[248px] flex-1">
      <Card title={title} height="100px">
        <div className="flex items-center">
          {amount && <PriceDisplay price={amount} />}
          {rate && <IncDecRate rate={rate} className={"ml-[16px]"} />}
        </div>
      </Card>
    </div>
  );
}
