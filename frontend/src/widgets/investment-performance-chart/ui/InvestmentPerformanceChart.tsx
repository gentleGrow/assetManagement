"use client";

import { LineChart, SegmentedButton, SegmentedButtonGroup } from "@/shared";
import { useState } from "react";
import PercentWithTitle from "./PercentWithTitle";

const PERFORMANCE_DATA = {
  dailyPerformanceData: {
    tooltipLabel: ["09:00", "13:00", "17:00", "21:00", "01:00", "05:00"],
    xAxises: ["09:00", "13:00", "17:00", "21:00", "01:00", "05:00"],
    values1: { values: [50, 0, 28, 0, 40, 45], name: "내 수익률" },
    values2: { values: [48, 28, 29, 34, 37, 42], name: "코스피" },
    unit: "%",
  },
  fiveDayPerformanceData: {
    tooltipLabel: ["02.28", "03.01", "03.02", "03.03", "03.04"],
    xAxises: ["02.28", "03.01", "03.02", "03.03", "03.04"],
    values1: { values: [60, 40, 38, 45, 50], name: "내 수익률" },
    values2: { values: [58, 38, 39, 44, 47], name: "코스피" },
    unit: "%",
  },
};

const PERIODS = [
  { period: "1일", performanceDataKey: "dailyPerformanceData" },
  { period: "5일", performanceDataKey: "fiveDayPerformanceData" },
  { period: "1달", performanceDataKey: "monthlyPerformanceData" },
  { period: "3달", performanceDataKey: "threeMonthPerformanceData" },
  { period: "6달", performanceDataKey: "sixMonthPerformanceData" },
  { period: "1년", performanceDataKey: "yearlyPerformanceData" },
];

export default function InvestmentPerformanceChart() {
  const [currentPerformanceDataKey, setCurrentPerformanceDataKey] =
    useState<string>("dailyPerformanceData");

  const currentData = PERFORMANCE_DATA[currentPerformanceDataKey];

  return (
    <div className="relative h-[388px] w-full rounded-xl border p-[16px] mobile:h-[500px] mobile:border-none">
      <h2 className="text-heading-2">투자 성과 분석</h2>
      <div className="mt-[16px] flex w-full justify-between except-mobile:absolute except-mobile:right-[16px] except-mobile:top-[12px] except-mobile:mt-0">
        <div className="w-[176px] shrink-0 mobile:hidden" />
        <div className="w-full except-mobile:w-[428px]">
          <SegmentedButtonGroup>
            {PERIODS.map((period) => (
              <SegmentedButton
                key={period.period}
                onClick={() =>
                  setCurrentPerformanceDataKey(period.performanceDataKey)
                }
              >
                {period.period}
              </SegmentedButton>
            ))}
          </SegmentedButtonGroup>
        </div>
      </div>
      <div className="flex h-full items-center mobile:flex-col except-mobile:justify-between">
        <div className="space-y-[32px] mobile:mt-[24px] mobile:flex mobile:w-full mobile:space-x-[16px] mobile:space-y-0">
          <PercentWithTitle title="내 수익률" percent={30.12} />
          <PercentWithTitle title="시장 수익률 대비" percent={8.57} />
        </div>
        <LineChart data={currentData} />
      </div>
    </div>
  );
}
