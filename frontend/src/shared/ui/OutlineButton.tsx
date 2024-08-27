import clsx from "clsx";
import { ReactNode } from "react";

export default function OutlineButton({
  title,
  className,
  isHover = false,
  isDisabled = false,
  children,
}: {
  title: string;
  className?: string;
  isHover?: boolean;
  isDisabled?: boolean;
  children?: ReactNode;
}) {
  const finalClassName = clsx(
    "relative h-[48px] w-[394px] rounded-md border text-center text-[16px] font-semibold leading-[24px] text-[#2A2D31] disabled:text-[#B9BCC1]",
    {
      "hover:border-[#999DA4]": !isDisabled,
      "border-[#D8DADC]": !isHover && !isDisabled,
      "border-[#999DA4]": isHover,
      "border-[#D8DADC] text-[#B9BCC1]": isDisabled,
    },
    className,
  );

  return (
    <button className={finalClassName} disabled={isDisabled}>
      <div className="absolute left-[16px] top-1/2 -translate-y-1/2">
        {children}
      </div>
      {title}
    </button>
  );
}
