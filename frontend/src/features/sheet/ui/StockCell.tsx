"use client";

import { useState, useEffect } from "react";
import Combobox from "@/widgets/combobox/ui/Combobox";

import { getAllStocks } from "@/features/sheet/api";

export default function StockCell({
  value,
  onChange,
}: {
  value?: { code: any; name: any };
  onChange?: (value: { id: string; name: string }) => void;
}) {
  const [stockList, setStockList] = useState<any[]>([]); // 데이터를 상태로 관리

  const fetchComboOptions = async () => {
    try {
      const stockList = await getAllStocks(); // API 호출
      setStockList(stockList); // 가져온 데이터를 상태로 설정
    } catch (error) {
      console.error("데이터를 불러오는 중 오류 발생:", error);
    }
  };

  useEffect(() => {
    fetchComboOptions();
  }, []);

  return <Combobox stocks={stockList} currentValue={value} />;
}
