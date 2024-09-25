// pages/asset/overview/page.tsx
import Summary from "@/widgets/card/Summary";

const Overview = () => {
  const SUMMARYDATA = [
    { title: "오늘의 review", type: "review" },
    { title: "나의 총 자산", type: "amount", amount: 12345600 },
    { title: "나의 투자 금액", type: "amount", amount: 976294 },
    { title: "수익금", type: "amount", amount: 1778123 },
  ];

  return (
    <div>
      <Summary summaryData={SUMMARYDATA} />
    </div>
  );
};

export default Overview;
