"use client"; // Client Component로 선언

import Tabs from "@/widgets/tab/Tabs"; // 새로 분리한 Tab 컴포넌트 가져오기

const AssetManagement: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const navItems = [
    { href: "/asset-management/sheet", label: "시트" },
    { href: "/asset-management/overview", label: "요약" },
  ];

  return (
    <div className="h-full py-[20px]">
      <div className="header px-[20px]">
        <Tabs items={navItems} />
        {/* timestamp */}
      </div>
      <div className="content h-[calc(100svh-64px)] min-w-[1080px] overflow-auto bg-gray-5 px-[20px] pt-[20px]">
        {children}
      </div>
    </div>
  );
};

export default AssetManagement;
