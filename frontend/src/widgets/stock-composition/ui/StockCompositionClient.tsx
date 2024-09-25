"use client";
import {
  DonutChart,
  DonutChartData,
  SegmentedButton,
  SegmentedButtonGroup,
} from "@/shared";
import { useState } from "react";
export default function StockCompositionClient({
  compositionData,
  accountData,
}: {
  compositionData: DonutChartData[];
  accountData: DonutChartData[];
}) {
  const [currentData, setCurrentData] = useState<any[]>(compositionData);

  return (
    <>
      <div className="mt-[16px] flex w-full except-mobile:absolute except-mobile:right-[16px] except-mobile:top-[12px] except-mobile:mt-0 except-mobile:w-[148px]">
        <SegmentedButtonGroup>
          <SegmentedButton onClick={() => setCurrentData(compositionData)}>
            종목별
          </SegmentedButton>
          <SegmentedButton onClick={() => setCurrentData(accountData)}>
            계좌별
          </SegmentedButton>
        </SegmentedButtonGroup>
      </div>
      <div className="mt-[48px] mobile:mt-[20px]">
        <DonutChart chartName="종목 구성" data={currentData} />
      </div>
    </>
  );
}
