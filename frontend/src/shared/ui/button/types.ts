import { colors } from "../themes/variables/colors/scale";

export type ButtonProps = {
  color?: keyof typeof colors;
  isDisabled?: boolean;
  isLoading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  size?: "xs" | "sm" | "md" | "lg" | "icon";
  variant?: "solid" | "outline" | "ghost" | "primary" | "icon";
} & React.ButtonHTMLAttributes<HTMLButtonElement>;
