"use client";
import { LeftArrowButton, RightArrowButton } from "@/shared";

export default function ArrowNavigator({
  navItems,
  currentNavItemIndex,
  handlerPrev,
  handlerNext,
}: {
  navItems: string[];
  currentNavItemIndex: number;
  handlerPrev: () => void;
  handlerNext: () => void;
}) {
  return (
    <div className="mx-auto flex w-full items-center justify-between">
      <LeftArrowButton
        onClick={() => {
          handlerPrev && handlerPrev();
        }}
        disabled={currentNavItemIndex === 0}
      />
      <p className="block text-body-3">{navItems[currentNavItemIndex]}</p>
      <RightArrowButton
        onClick={() => {
          handlerNext && handlerNext();
        }}
        disabled={currentNavItemIndex === navItems.length - 1}
      />
    </div>
  );
}
