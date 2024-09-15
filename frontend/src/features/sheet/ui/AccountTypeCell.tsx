"use client";
import { useState, useEffect } from "react";
import Listbox from "@/widgets/listbox/ui/Listbox";
import { getAllOptions } from "@/features/sheet/api";

export default function AccountTypeCell({
  value,
  onChange,
}: {
  value?: { id: string; name: string };
  onChange?: (value: { id: string; name: string }) => void;
}) {
  const [accountList, setAccountList] = useState<any[]>([]);

  const fetchOptions = async () => {
    try {
      const { accountList } = await getAllOptions();
      setAccountList(accountList);
    } catch (error) {
      console.error("데이터를 불러오는 중 오류 발생:", error);
    }
  };

  useEffect(() => {
    fetchOptions();
  }, []);

  return <Listbox options={accountList} />;
}
