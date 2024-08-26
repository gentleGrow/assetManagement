import { Text as _Text } from "@/shared/ui/layout/src";
import { text } from "@/shared/ui/themes/classes/typography";
import { colors } from "@/shared/ui/themes/variables/colors/scale";

export default {
  title: "React Components/Layout/Typography/Text",
  component: _Text,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
  argTypes: {
    as: {
      options: ["p", "span", "div", "b", "i", "u", "strong", "em"],
      control: "select",
    },
    fontSize: {
      options: Object.keys(text),
      control: "select",
    },
    color: {
      options: Object.keys(colors),
      control: "select",
    },
  },
};

export const Text = {
  args: {
    as: "p",
    children: "Hello World",
    fontSize: "xl",
    color: "gray",
    background: "blue",
  },
};
