import * as React from "react";
import { forwardRef, Ref } from "react";
import { headingStyle } from "./style.css";
import { HeadingProps } from "./types";
import { clsx } from "clsx";
import { extractSprinkleProps } from "../utils/properties";
import { BaseStyle, StyleSprinkles } from "../../style.css";

const Heading = (props: HeadingProps, ref: Ref<HTMLElement>) => {
  const { as = "h1", fontSize, background, children } = props;
  const backgroundColor = background ? background : undefined;

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
        headingStyle({
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

const _Heading = forwardRef(Heading);
export { _Heading as Heading };
