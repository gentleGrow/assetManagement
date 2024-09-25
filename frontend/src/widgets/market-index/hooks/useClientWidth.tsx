"use client";
import { useEffect, useState } from "react";
const useClientWidth = () => {
  const getWindowClientWidth = (): number => {
    const { innerWidth } = window;
    return innerWidth;
  };
  const [clientWidth, setClientWidth] = useState<number>(
    getWindowClientWidth(),
  );
  useEffect(() => {
    const handleResize = () => {
      setClientWidth(getWindowClientWidth());
    };
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);
  return clientWidth;
};

export default useClientWidth;
