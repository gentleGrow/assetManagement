"use client";

import { useState, useEffect } from "react";
import Summary from "@/widgets/card/Summary";
import DraggableTable from "@/features/sheet/ui/DraggableTable";
import { getStockAssets } from "@/features/sheet/api";

const Sheet = () => {
  const [summaryData, setSummaryData] = useState<any>([]);
  const [tableData, setTableData] = useState<any[]>([]);

  const fetchData = async () => {
    try {
      const {
        stock_assets,
        total_asset_amount,
        total_invest_amount,
        total_profit_rate,
        total_profit_amount,
        total_dividend_amount,
      } = await getStockAssets();

      setTableData(stock_assets);
      setSummaryData({
        total_asset_amount: total_asset_amount,
        total_invest_amount: total_invest_amount,
        total_profit_amount: total_profit_amount,
        total_dividend_amount: total_dividend_amount,
      });
    } catch (error) {
      console.error("데이터를 불러오는 중 오류 발생:", error);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div>
      <Summary summaryData={summaryData} />
      <DraggableTable tableData={tableData} setTableData={setTableData} />
    </div>
  );
};

export default Sheet;
