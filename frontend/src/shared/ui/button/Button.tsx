import * as React from "react";
import { clsx } from "clsx";
import { assignInlineVars } from "@vanilla-extract/dynamic";
import {
  activeColorVariant,
  buttonStyle,
  enableColorVariant,
  hoverColorVariant,
  spanStyle,
  spinnerStyle,
} from "./style.css";
import { ButtonProps } from "./types";
import { useButton } from "./hooks/useButton";
import { colors } from "../themes/variables";


const Button = (props: ButtonProps, ref: React.Ref<HTMLButtonElement>) => {
  const { buttonProps } = useButton(props);

  const {
    variant = "solid",
    size = "md",
    color = "gray",
    leftIcon,
    rightIcon,
    isLoading,
    children,
    style,
  } = props;

  const endableColor =colors.$scale[color][50];
  const hoverColor =
    variant === "solid"
      ? colors.$scale[color][60]
      : colors.$scale[color][50];
  const activeColor =
    variant === "solid"
      ? colors.$scale[color][70]
      : colors.$scale[color][10];

  return (
    <button
      {...buttonProps}
      // 기능 ^
      ref={ref}
      className={clsx([
        buttonStyle({
          size,
          variant,
        }),
      ])}
      style={{
        ...assignInlineVars({
          [enableColorVariant]: endableColor,
          [hoverColorVariant]: hoverColor,
          [activeColorVariant]: activeColor,
        }),
        ...style,
      }}
    >
      {isLoading && <div className={spinnerStyle({ size })} />}
      {leftIcon && <span className={spanStyle({ size })}>{leftIcon}</span>}
      <span>{children}</span>
      {rightIcon && <span className={spanStyle({ size })}>{rightIcon}</span>}
    </button>
  );
};

const _Button = React.forwardRef(Button);
export { _Button as Button };
