"use client";
import Listbox from "@/widgets/listbox/ui/Listbox";

export default function AccountTypeCell({
  value,
  onChange,
  accountList,
}: {
  value?: any;
  onChange?: (value: any) => void;
  accountList?: any[];
}) {
  const handleChange = (value: { id: string; name: string }) => {
    if (onChange) {
      onChange(value.name);
    }
  };

  return (
    <Listbox
      options={accountList ?? []}
      currentValue={{ id: value, name: value }}
      onChange={handleChange}
    />
  );
}
