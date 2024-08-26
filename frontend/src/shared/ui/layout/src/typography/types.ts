import { CSSProperties } from "@vanilla-extract/css";
import { heading, text } from "../../../themes/classes/typography";
import { AsElementProps, StyleProps } from "../../types";

export type TextProps = AsElementProps &
  StyleProps & {
    fontSize: keyof typeof text;
    align?: CSSProperties["textAlign"];
    casing?: CSSProperties["textTransform"];
    decoration?: CSSProperties["textDecoration"];
  };

export type HeadingProps = StyleProps &
  AsElementProps & {
    fontSize: keyof typeof heading;
  };
