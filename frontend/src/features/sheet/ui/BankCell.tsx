"use client";
import Listbox from "@/widgets/listbox/ui/Listbox";

export default function BankCell({
  value,
  onChange,
  bankList,
}: {
  value?: any;
  onChange?: (value: any) => void;
  bankList?: any[];
}) {

  const handleChange = (value: { id: string; name: string }) => {
    if (onChange) {
      onChange(value.name);
    }
  };

  return (
    <Listbox
      options={bankList ?? []}
      iconPath="/images/securities.svg"
      currentValue={{ id: value, name: value }}
      onChange={handleChange}
    />
  );
}
