"use client";

import { useEffect, useState } from "react";

export default function VerticalTicker({ items }: { items: any[] }) {
  const [currentItem, setCurrentItem] = useState<number>(0);
  const [className, setClassName] = useState<string>("");
  useEffect(() => {
    const handleAnimation = async () => {
      setClassName("transition-all duration-500 -translate-y-full opacity-0");
      await new Promise((resolve) => setTimeout(resolve, 500));
      setClassName("translate-y-full opacity-0");
      setCurrentItem((prevItem) => (prevItem + 1) % items.length);
      await new Promise((resolve) => setTimeout(resolve, 100));
      setClassName("transition-all duration-500 translate-y-0 opacity-100");
    };

    const timerId = setInterval(handleAnimation, 4000);
    return () => clearInterval(timerId);
  }, [items]);
  return (
    <div className="flex">
      <div className={"flex items-center " + className}>
        {items[currentItem]}
      </div>
    </div>
  );
}
