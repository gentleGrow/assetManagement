import Listbox from "@/widgets/listbox/ui/Listbox";

export default function BankCell({
  value,
  onChange,
}: {
  value: { id: string; name: string };
  onChange: (value: { id: string; name: string }) => void;
}) {
  const banks = [
    { id: "1", name: "국민은행" },
    { id: "2", name: "신한은행" },
    { id: "3", name: "우리은행" },
  ];

  return <Listbox options={banks} iconPath="/images/securities.svg" />;
}
