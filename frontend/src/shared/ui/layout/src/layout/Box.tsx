import * as React from "react";
import { BoxProps } from "./types";
import { clsx } from "clsx";
import { extractSprinkleProps } from "../utils/properties";
import { BaseStyle, StyleSprinkles } from "../../style.css";
import { Color, colors } from "../../../themes/variables/colors/scale";

const Box = (props: BoxProps, ref: React.Ref<HTMLElement>) => {
  const { as = "div", color, background, children } = props;
  const backgroundColor = colors[color as Color]?.[70];
  const colorStyle = colors[color as Color]?.[10];
  return React.createElement(
    as,
    {
      ...props,
      ref,
      className: clsx([
        BaseStyle,
        StyleSprinkles(
          extractSprinkleProps(props, Array.from(StyleSprinkles.properties)),
        ),
        props.className,
      ]),
      style: {
        color: colorStyle,
        background: backgroundColor,
        ...props.style,
      },
    },
    children,
  );
};

const _Box = React.forwardRef(Box);
export { _Box as Box };
