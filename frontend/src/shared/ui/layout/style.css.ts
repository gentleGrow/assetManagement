import { style } from "@vanilla-extract/css";
import { defineProperties, createSprinkles } from "@vanilla-extract/sprinkles";
import { radii, shadows, spacing } from "../themes/variables/box";

export const BaseStyle = style({
  // @ts-ignore
  "&:focus-visible": {
    outline: "none",

    boxShadow: shadows.outline,
  },
});

const MarginAndPaddingProperties = defineProperties({
  properties: {
    marginTop: spacing,
    marginRight: spacing,
    marginBottom: spacing,
    marginLeft: spacing,
    paddingTop: spacing,
    paddingRight: spacing,
    paddingBottom: spacing,
    paddingLeft: spacing,
  },
  shorthands: {
    margin: ["marginTop", "marginRight", "marginBottom", "marginLeft"],
    padding: ["paddingTop", "paddingRight", "paddingBottom", "paddingLeft"],
    marginX: ["marginLeft", "marginRight"],
    marginY: ["marginTop", "marginBottom"],
    paddingX: ["paddingLeft", "paddingRight"],
    paddingY: ["paddingTop", "paddingBottom"],
  },
});

const BorderStyleProperties = defineProperties({
  properties: {
    borderRadius: radii,
  },
});

const BoxShadowStyleProps = defineProperties({
  properties: {
    boxShadow: shadows,
  },
});

export const StyleSprinkles = createSprinkles(
  MarginAndPaddingProperties,
  BorderStyleProperties,
  BoxShadowStyleProps,
);