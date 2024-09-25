"use client";
import DonutChart from "./DonutChart";

export default function PortfolioItem({ item, chartName }) {
  return (
    <div className="h-[244px] shrink-0">
      <div className="h-full rounded-lg border p-[16px]">
        <h3 className="mb-[8px] truncate text-body-3">{item.name}</h3>
        <div className="h-[180px]">
          <DonutChart
            data={item.data}
            chartName={chartName}
            isPortfolio={true}
          />
        </div>
      </div>
    </div>
  );
}
