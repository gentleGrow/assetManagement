export type Color = 'gray' | 'green';
type Shade = 10 | 20 | 30 | 40 | 50 | 60 | 70 | 80 | 90 | 100 | 0 | 5;

type ColorScale = {
  [key in Shade]?: string; 
};

export const green: ColorScale = {
  10: "var(--green-10)",
  20: "var(--green-20)",
  30: "var(--green-30)",
  40: "var(--green-40)",
  50: "var(--green-50)",
  60: "var(--green-60)",
  70: "var(--green-70)",
  80: "var(--green-80)",
  90: "var(--green-90)",
  100: "var(--green-100)",
};

export const gray: ColorScale = {
  0: "var(--gray-0)",
  5: "var(--gray-5)",
  10: "var(--gray-10)",
  20: "var(--gray-20)",
  30: "var(--gray-30)",
  40: "var(--gray-40)",
  50: "var(--gray-50)",
  60: "var(--gray-60)",
  70: "var(--gray-70)",
  80: "var(--gray-80)",
  90: "var(--gray-90)",
};

export const colors: Record<Color, ColorScale> = {
  gray,
  green,
};
