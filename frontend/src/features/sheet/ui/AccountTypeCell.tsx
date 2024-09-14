import Listbox from "@/widgets/listbox/ui/Listbox";

export default function AccountTypeCell({
  value,
  onChange,
}: {
  value: { id: string; name: string };
  onChange: (value: { id: string; name: string }) => void;
}) {
  const accountTypes = [{ id: "1", name: "ISA" }];

  return <Listbox options={accountTypes} />;
}
