import { recipe } from "@vanilla-extract/recipes";
import { createVar, keyframes } from "@vanilla-extract/css";
import { radii, shadows } from "../themes/variables/box";
import { text } from "../themes/classes/typography";
import { fontSize, fontWeight } from "../themes/variables/typography";
import { colors } from "../themes/variables";

export const enableColorVariant = createVar(); // 500
export const hoverColorVariant = createVar(); // 600 outline 50 ghost 50
export const activeColorVariant = createVar(); // 700 outline 100 ghost 100

export const buttonStyle = recipe({
  base: {
    margin: 0,
    padding: 0,
    border: 0,

    borderRadius: "6px",
    // borderRadius: radii.md,
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    cursor: "pointer",
    userSelect: "none",
    transition: "background-color 0.2s, color 0.2s, border-color 0.2s",
    // @ts-ignore
    "&[disabled]": {
      opacity: 0.4,
      cursor: "not-allowed",
    },
    '&[data-loading="true"]': {
      "& span": {
        opacity: 0,
      },
    },
    "&:focus-visible": {
      outline: "none",

      boxShadow: shadows.outline,
    },
  },
  variants: {
    size: {
      xs: {
        ...text.xs,
        fontWeight: fontWeight[600],
        padding: "0 0.5rem",
        gap: "0.5rem",
        height: "1.5rem",
      },
      sm: {
        ...text.sm,
        fontWeight: fontWeight[600],
        padding: "0 0.75rem",
        gap: "0.5rem ",
        height: "2rem",
      },
      md: {
        ...text.sm,
        padding: "8px 12px",
        gap: "10px",
        height: "36px",
        width: "182px",
        // padding: "0 1rem",
        // gap: "0.5rem",
        // height: "2.5rem",
      },
      lg: {
        ...text.lg,
        fontWeight: fontWeight[600],
        padding: "0 1.5rem",
        gap: "0.5rem",
        height: "3rem",
      },
    },
    variant: {
      primary: {
        backgroundColor: colors.$scale.green[60],
        color: "#FFFFFF",

        "&:hover:not([disabled])": {
          backgroundColor: colors.$scale.green[70],
        },
        "&:active:not([disabled])": {
          backgroundColor: colors.$scale.green[70],
        },
        "&[disabled]": {
          backgroundColor: colors.$scale.gray[10],
          color: colors.$scale.gray[50],
          opacity: 1,
          cursor: "not-allowed",
        },
      },
      solid: {
        backgroundColor: enableColorVariant,
        color: colors.$scale.gray[50],

        "&:hover:not([disabled])": {
          backgroundColor: hoverColorVariant,
        },
        "&:active:not([disabled])": {
          backgroundColor: activeColorVariant,
        },
      },
      outline: {
        border: `1px solid ${enableColorVariant}`,
        color: enableColorVariant,

        "&:hover:not([disabled])": {
          backgroundColor: hoverColorVariant,
        },
        "&:active:not([disabled])": {
          backgroundColor: activeColorVariant,
        },
      },
      ghost: {
        color: enableColorVariant,

        "&:hover:not([disabled])": {
          backgroundColor: hoverColorVariant,
        },
        "&:active:not([disabled])": {
          backgroundColor: activeColorVariant,
        },
      },
    },
  },
});

export const spanStyle = recipe({
  base: {
    display: "flex",
    alignItems: "center",
  },
  variants: {
    size: {
      xs: {
        ...text.xs,
        fontWeight: fontWeight[600],
      },
      sm: {
        ...text.sm,
        fontWeight: fontWeight[600],
      },
      md: {
        ...text.md,
        fontWeight: fontWeight[600],
      },
      lg: {
        ...text.lg,
        fontWeight: fontWeight[600],
      },
    },
  },
});

const spinKeyframes = keyframes({
  "0%": { transform: "rotate(0deg)" },
  "100%": { transform: "rotate(360deg)" },
});

export const spinnerStyle = recipe({
  base: {
    position: "absolute",
    animation: `${spinKeyframes} 0.45s linear infinite`,
    display: "inline-block",
    borderTop: "2px solid currentcolor",
    borderRight: "2px solid currentcolor",
    borderBottom: "2px solid transparent",
    borderLeft: "2px solid transparent",
    borderRadius: "50%",
  },
  variants: {
    size: {
      xs: {
        width: fontSize[12],
        height: fontSize[12],
        left: `calc(50% - ${fontSize[12]}/2)`,
      },
      sm: {
        width: fontSize[14],
        height: fontSize[14],
        left: `calc(50% - ${fontSize[14]}/2)`,
      },
      md: {
        width: fontSize[16],
        height: fontSize[16],
        left: `calc(50% - ${fontSize[16]}/2)`,
      },
      lg: {
        width: fontSize[18],
        height: fontSize[18],
        left: `calc(50% - ${fontSize[18]}/2)`,
      },
    },
  },
});
