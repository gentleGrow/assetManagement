import { ReactNode } from "react";

interface CardProps {
  children: ReactNode; // children prop의 타입 정의
  title?: string;
  width?: string; // 너비를 위한 prop 추가
  height?: string; // 높이를 위한 prop 추가
}

export default function Card({ children, title, width, height }: CardProps) {
  return (
    <div
      className="flex flex-col justify-between rounded-lg border bg-white p-4"
      style={{ width: width, height: height }}
    >
      {title && (
        <h2 className="text-[16px] font-bold leading-[19px]">{title}</h2>
      )}
      {children}
    </div>
  );
}
