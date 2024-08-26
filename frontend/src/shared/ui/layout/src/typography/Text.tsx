import * as React from "react";
import { TextProps } from "./types";
import { clsx } from "clsx";
import { extractSprinkleProps } from "../utils/properties";
import { textStyle } from "./style.css";
import { BaseStyle, StyleSprinkles } from "../../style.css";
import { Color, colors } from "../../../themes/variables/colors/scale";

const Text = (props: TextProps, ref: React.Ref<HTMLElement>) => {
  const { as = "p", color = "gray", background, children, fontSize } = props;
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
        textStyle({
          fontSize,
        }),
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

const _Text = React.forwardRef(Text);
export { _Text as Text };
