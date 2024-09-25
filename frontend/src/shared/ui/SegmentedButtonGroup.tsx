"use client";
import React, { ReactNode, useState } from "react";
import { SegmentedButtonProps } from "../types/component-props";

export default function SegmentedButtonGroup({
  children,
}: {
  children: ReactNode;
}) {
  const [selectedIndex, setSelectedIndex] = useState<number | null>(0);
  const childrenArray = React.Children.toArray(children);
  const handleClick = (index: number, onClick?: () => void) => {
    setSelectedIndex(index);
    if (onClick) {
      onClick();
    }
  };

  return (
    <div className="flex w-full rounded-md bg-gray-10 p-[4px]">
      {childrenArray.map((child, index) => {
        if (React.isValidElement<SegmentedButtonProps>(child)) {
          return React.cloneElement(child, {
            numberOfButtons: childrenArray.length,
            isSelected: selectedIndex === index,
            onClick: () => handleClick(index, child.props.onClick),
          });
        }
        return child;
      })}
    </div>
  );
}
