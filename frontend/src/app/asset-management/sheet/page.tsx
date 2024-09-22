"use client";

import { useState, useEffect } from "react";
import Summary from "@/widgets/card/Summary";
import DraggableTable from "@/features/sheet/ui/DraggableTable";
import TableHeader from "@/features/sheet/ui/TableHeader";
import { getStockAssets } from "@/features/sheet/api";

const Sheet = () => {
  const [summaryData, setSummaryData] = useState<any>([]);
  const [tableData, setTableData] = useState<any[]>([]);
  const [count, setCount] = useState(0);

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
      setCount(stock_assets.length);
      setSummaryData({
        total_asset_amount: total_asset_amount,
        total_invest_amount: total_invest_amount,
        total_profit_rate: total_profit_rate,
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
    <>
      <Summary summaryData={summaryData} />
      <TableHeader count={count} />
      <DraggableTable tableData={tableData} setTableData={setTableData} />
    </>
  );
};

export default Sheet;
