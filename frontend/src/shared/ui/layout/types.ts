import { colors } from "../themes/variables/colors/scale";
import { StyleSprinkles } from "./style.css";

type AsProps = {
  as?: Exclude<keyof JSX.IntrinsicElements, keyof SVGElementTagNameMap>;
};

type ElementProps = Omit<React.HTMLAttributes<HTMLElement>, "as">;

export type AsElementProps = AsProps & ElementProps;

export type ColorProps = {
  color?: keyof typeof colors;
  background?: keyof typeof colors
};

export type StyleProps = Parameters<typeof StyleSprinkles>[0] & ColorProps;
