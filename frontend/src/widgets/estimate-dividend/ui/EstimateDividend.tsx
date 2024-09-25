"use client";
import {
  BarChart,
  DonutChart,
  SegmentedButton,
  SegmentedButtonGroup,
} from "@/shared";
import { useState } from "react";
import ArrowNavigator from "./ArrowNavigator";
const barChartData = {
  "2022": {
    xAxises: [
      "1월",
      "2월",
      "3월",
      "4월",
      "5월",
      "6월",
      "7월",
      "8월",
      "9월",
      "10월",
      "11월",
      "12월",
    ],
    data: [8, 12, 18, 22, 26, 30, 34, 38, 42, 46, 50, 54],
    unit: "만원",
    total: 390,
  },
  "2023": {
    xAxises: [
      "1월",
      "2월",
      "3월",
      "4월",
      "5월",
      "6월",
      "7월",
      "8월",
      "9월",
      "10월",
      "11월",
      "12월",
    ],
    data: [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60],
    unit: "만원",
    total: 390,
  },
  "2024": {
    xAxises: [
      "1월",
      "2월",
      "3월",
      "4월",
      "5월",
      "6월",
      "7월",
      "8월",
      "9월",
      "10월",
      "11월",
      "12월",
    ],
    data: [6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72],
    unit: "만원",
    total: 468,
  },
};

const donutChartData = [
  {
    name: "Apple Inc.",
    percent_rate: 9.92712353499655,
    current_amount: 1728443.4749999999,
  },
  {
    name: "Microsoft Corporation",
    percent_rate: 35.83470637001111,
    current_amount: 6239296.225682373,
  },
  {
    name: "Amazon.com, Inc.",
    percent_rate: 4.190222190506732,
    current_amount: 729573.0911828614,
  },
  {
    name: "Alphabet Inc. (Class A)",
    percent_rate: 4.778454887165491,
    current_amount: 831992.1819433593,
  },
  {
    name: "Tesla, Inc.",
    percent_rate: 8.568279580717842,
    current_amount: 1491850.7744018557,
  },
  {
    name: "Meta Platforms, Inc.",
    percent_rate: 24.17584206823141,
    current_amount: 4209333.784167481,
  },
  {
    name: "NVIDIA Corporation",
    percent_rate: 6.171944041816169,
    current_amount: 1074617.0700439452,
  },
  {
    name: "Schwab U.S. Dividend Equity ETF",
    percent_rate: 6.353427326554699,
    current_amount: 1106215.7096923827,
  },
];

export default function EstimateDividend() {
  const [selectedTab, setSelectedTab] = useState<string>("모두");
  const barChartNavItems = Object.keys(barChartData);
  const [currentNavItemIndex, setCurrentNavItemIndex] = useState<number>(
    barChartNavItems.length - 1,
  );
  return (
    <div
      className={`relative ${selectedTab === "모두" ? "h-[388px]" : "h-full"} w-full rounded-xl border p-[16px] ${selectedTab === "모두" ? "mobile:h-[500px]" : "h-full"} mobile:border-none`}
    >
      <h2 className="text-heading-2">예상 배당액</h2>
      <div className="mt-[16px] flex w-full justify-between except-mobile:absolute except-mobile:right-[16px] except-mobile:top-[12px] except-mobile:mt-0">
        <div className="w-[176px] shrink-0 mobile:hidden" />
        <div className="w-full except-mobile:w-[148px]">
          <SegmentedButtonGroup>
            <SegmentedButton onClick={() => setSelectedTab("모두")}>
              모두
            </SegmentedButton>
            <SegmentedButton onClick={() => setSelectedTab("종목별")}>
              종목별
            </SegmentedButton>
          </SegmentedButtonGroup>
        </div>
      </div>
      {selectedTab === "모두" && (
        <>
          <div className="mb-[16px] mt-[20px]">
            <ArrowNavigator
              navItems={barChartNavItems}
              currentNavItemIndex={currentNavItemIndex}
              handlerPrev={() => {
                setCurrentNavItemIndex((prev) => prev - 1);
              }}
              handlerNext={() => {
                setCurrentNavItemIndex((prev) => prev + 1);
              }}
            />
          </div>
          <div className="space-y-[4px]">
            <p className="text-body-3">
              {barChartNavItems[currentNavItemIndex]}년 총 배당액
            </p>
            <p className="text-[28px] font-bold leading-[33.61px]">
              ₩
              {(
                barChartData[barChartNavItems[currentNavItemIndex]].total *
                10000
              ).toLocaleString("ko-KR")}
            </p>
          </div>
        </>
      )}

      <div
        className={`${selectedTab === "모두" ? "h-[217px]" : "h-full"} w-full`}
      >
        {selectedTab === "모두" ? (
          <BarChart
            chartData={{
              ...(({ sum, ...rest }) => rest)(
                barChartData[barChartNavItems[currentNavItemIndex]],
              ),
            }}
          />
        ) : (
          <div className="py-[41px]">
            <DonutChart chartName="예상 배당액" data={donutChartData} />
          </div>
        )}
      </div>
    </div>
  );
}
