"use client";
import { useState, useEffect } from "react";
import Listbox from "@/widgets/listbox/ui/Listbox";
import { getAllOptions } from "@/features/sheet/api";

export default function BankCell({
  value,
  onChange,
}: {
  value?: { id: string; name: string };
  onChange?: (value: { id: string; name: string }) => void;
}) {
  const [bankList, setBankList] = useState<any[]>([]);

  const fetchOptions = async () => {
    try {
      const { bankList } = await getAllOptions();
      setBankList(bankList);
    } catch (error) {
      console.error("데이터를 불러오는 중 오류 발생:", error);
    }
  };

  useEffect(() => {
    fetchOptions();
  }, []);

  return <Listbox options={bankList} iconPath="/images/securities.svg" />;
}
