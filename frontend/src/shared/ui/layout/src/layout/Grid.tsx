import * as React from "react";
import { GridProps } from "./types";
import { clsx } from "clsx";
import { extractSprinkleProps } from "../utils/properties";
import { BaseStyle, StyleSprinkles } from "../../style.css";
import { Color, colors } from "../../../themes/variables/colors/scale";

const Grid = (props: GridProps, ref: React.Ref<HTMLElement>) => {
  const {
    as = "div",
    color,
    background,
    children,
    autoColumns,
    autoFlow,
    autoRows,
    columnGap,
    column,
    gap,
    row,
    rowGap,
    templateColumns,
    templateRows,
    templateAreas,
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
        display: "grid",
        gridAutoColumns: autoColumns,
        gridAutoFlow: autoFlow,
        gridAutoRows: autoRows,
        gridColumnGap: columnGap,
        gridGap: gap,
        gridRowGap: rowGap,
        gridTemplateColumns: templateColumns,
        gridTemplateRows: templateRows,
        gridTemplateAreas: templateAreas,
        gridColumn: column,
        gridRow: row,
        color: colorStyle,
        background: backgroundColor,
        ...props.style,
      },
    },
    children,
  );
};

const _Grid = React.forwardRef(Grid);
export { _Grid as Grid };
