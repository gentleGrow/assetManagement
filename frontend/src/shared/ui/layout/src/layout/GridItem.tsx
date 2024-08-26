import * as React from "react";
import { GridItemProps } from "./types";
import { clsx } from "clsx";
import { extractSprinkleProps } from "../utils/properties";
import { BaseStyle, StyleSprinkles } from "../../style.css";
import { Color, colors } from "../../../themes/variables/colors/scale";


const GridItem = (props: GridItemProps, ref: React.Ref<HTMLElement>) => {
  const {
    as = "div",
    color,
    background,
    children,
    area,
    colEnd,
    colStart,
    colSpan,
    rowEnd,
    rowStart,
    rowSpan,
  } = props;
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
        gridArea: area,
        gridColumnEnd: colEnd,
        gridColumnStart: colStart,
        gridColumn: colSpan,
        gridRowEnd: rowEnd,
        gridRowStart: rowStart,
        gridRow: rowSpan,
        color: colorStyle,
        background: backgroundColor,
        ...props.style,
      },
    },
    children,
  );
};

const _GridItem = React.forwardRef(GridItem);
export { _GridItem as GridItem };
