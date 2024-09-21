"use client";

import Input from "@/shared/ui/Input";

export default function NumberCell({
  value,
  onChange,
}: {
  value?: any;
  onChange?: (value: any) => void;
}) {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { value } = e.target;
    if (onChange) {
      onChange(value);
    }
  };
  return <Input type="text" value={value} onChange={handleChange} />;
}
