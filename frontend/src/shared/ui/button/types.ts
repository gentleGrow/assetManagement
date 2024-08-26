import { colors } from "../themes/variables/colors/scale";

export type ButtonProps = {
  color?: keyof typeof colors;
  isDisabled?: boolean;
  isLoading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  size?: "xs" | "sm" | "md" | "lg";
  variant?: "solid" | "outline" | "ghost";
} & React.ButtonHTMLAttributes<HTMLButtonElement>;
