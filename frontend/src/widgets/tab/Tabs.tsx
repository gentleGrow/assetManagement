import Link from "next/link";
import { usePathname } from "next/navigation";

interface TabsProps {
  items: { href: string; label: string }[]; // 탭 항목 배열
}

const Tabs: React.FC<TabsProps> = ({ items }) => {
  const pathname = usePathname(); // 현재 경로 가져오기

  return (
    <ul className="flex space-x-2.5">
      {items.map(({ href, label }) => (
        <li key={href}>
          <Link
            href={href}
            className={`px-[12px] py-[6px] text-lg ${
              pathname === href
                ? "border-b-[3px] border-black font-bold text-gray-100"
                : "font-normal text-gray-60"
            }`}
          >
            {label}
          </Link>
        </li>
      ))}
    </ul>
  );
};

export default Tabs;
