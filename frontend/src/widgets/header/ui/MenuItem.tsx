import Link from "next/link";
import Selected from "./Selected";
import MenuName from "./MenuName";
export default function MenuItem({
  name,
  href,
  isSelected,
  isHovered = false,
}: {
  name: string;
  href: string;
  isSelected: boolean;
  isHovered?: boolean;
}) {
  return (
    <Link href={href} className="relative">
      <Selected isSelected={isSelected} />
      <MenuName name={name} isHovered={isHovered} />
    </Link>
  );
}
