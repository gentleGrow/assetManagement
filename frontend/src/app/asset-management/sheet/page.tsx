"use client";

import { useState, useEffect } from "react";
import Summary from "@/widgets/card/Summary";
import DraggableTable from "@/features/sheet/ui/DraggableTable";
import TableHeader from "@/features/sheet/ui/TableHeader";
import { getStockAssets, getAssetFields } from "@/features/sheet/api";

const Sheet = () => {
  const [summaryData, setSummaryData] = useState<any>([]);
  const [tableData, setTableData] = useState<any[]>([]);
  const [fieldList, setFieldList] = useState<string[]>([]);
  const [count, setCount] = useState(0);
  const [isKRW, setIsKRW] = useState<boolean>(true);

  const fetchData = async () => {
    try {
      const {
        stock_assets,
        total_asset_amount,
        total_invest_amount,
        total_profit_rate,
        total_profit_amount,
        total_dividend_amount,
      } = await getStockAssets(isKRW);

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

  const fetchFields = async () => {
    try {
      const data = await getAssetFields();
      setFieldList(data);
    } catch (error) {
      console.error("데이터를 불러오는 중 오류 발생:", error);
    }
  };

  useEffect(() => {
    fetchData();
    fetchFields();
  }, []);

  const changeCurrency = (value) => {
    setIsKRW(value);
    fetchData();
  };

  return (
    <>
      <Summary summaryData={summaryData} />
      <TableHeader count={count} changeCurrency={changeCurrency} />
      <DraggableTable
        tableData={tableData}
        setTableData={setTableData}
        fieldList={fieldList}
        fetchData={fetchData}
      />
    </>
  );
};

export default Sheet;
