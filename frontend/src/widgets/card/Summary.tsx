"use client";

import { useState, useEffect } from "react";
import SummaryCard from "./SummaryCard";

const SUMMARYDATA = [
  {
    title: "총 자산",
    id: "total_asset_amount",
    type: "amount",
    amount: 0,
  },
  {
    title: "투자 금액",
    id: "total_invest_amount",
    type: "amount",
    amount: 0,
  },
  {
    title: "수익금",
    id: "total_profit_amount",
    type: "amount",
    amount: 0,
    rate: "total_profit_rate",
  },
  {
    title: "배당금",
    id: "total_dividend_amount",
    type: "amount",
    amount: 0,
    rate: "total_profit_rate",
  },
];

export default function Summary({ summaryData }: any) {
  const [summary, setSummary] = useState<any>(SUMMARYDATA);

  useEffect(() => {
    const newSummaryData = SUMMARYDATA.map((data) => {
      const summary = {
        ...data,
        amount: summaryData[data.id] || 0,
      };

      if (data?.rate) {
        summary.rate = summaryData[data.rate] || 0;
      }

      return summary;
    });
    setSummary(newSummaryData);
  }, [summaryData]);

  return (
    <div className="flex space-x-[16px]">
      {summary.map(({ title, type, amount, rate }) => (
        <SummaryCard
          key={title}
          title={title}
          type={type}
          amount={amount}
          rate={rate}
        />
      ))}
    </div>
  );
}
