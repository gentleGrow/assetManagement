import { green } from "@/shared/ui/themes/variables/colors/static/light";

export default function Selected({ isSelected }: { isSelected: boolean }) {
  if (!isSelected) return null;

  return (
    <div
      className="absolute -top-[8px] left-1/2 h-[5px] w-[5px] -translate-x-1/2 rounded-full"
      style={{ backgroundColor: green[50] }}
    />
  );
}
