"use client";
import { usePathname } from "next/navigation";
import MenuItem from "./MenuItem";

const MENUS = [
  { name: "홈", href: "/" },
  { name: "자산관리", href: "/asset-management/sheet" },
];

export default function Menu({
  selectedItem = "",
  hoveredItem = "",
}: {
  selectedItem?: string;
  hoveredItem?: string;
}) {
  const pathname = usePathname() || "";
  return (
    <nav className="flex space-x-[150px]">
      {MENUS.map((menu) => {
        const isSelected =
          selectedItem.includes(menu.name) ||
          (menu.href === "/" ? pathname === "/" : pathname.includes(menu.href));

        const isHovered = hoveredItem.includes(menu.name);

        return (
          <div key={menu.name} className="flex items-center">
            <MenuItem
              name={menu.name}
              href={menu.href}
              isSelected={isSelected}
              isHovered={isHovered}
            />
          </div>
        );
      })}
    </nav>
  );
}
