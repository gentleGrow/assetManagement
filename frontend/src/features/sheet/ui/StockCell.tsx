"use client";

import Combobox from "@/widgets/combobox/ui/Combobox";

export default function StockCell({
  value,
  code,
  onChange,
}: {
  value?: string;
  code?: string;
  onChange?: (value: any) => void;
}) {
  const handleChange = (value: { code: string; name: string }) => {
    if (onChange) {
      onChange({ stock_code: value.code, stock_name: value.name });
    }
  };
  return (
    <Combobox
      currentValue={{ code: code, name: value }}
      onChange={handleChange}
    />
  );
}
