import { Heading as _Heading } from "@/shared/ui/layout/src";
import { heading } from "@/shared/ui/themes/classes/typography";
import { colors } from "@/shared/ui/themes/variables/colors/scale";

export default {
  title: "React Components/Layout/Typography/Heading",
  component: _Heading,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
  argTypes: {
    as: {
      options: ["h1", "h2", "h3", "h4", "h5", "h6"],
      control: "select",
    },
    fontSize: {
      options: Object.keys(heading),
      control: "select",
    },
    color: {
      options: Object.keys(colors),
      control: "select",
    },
  },
};

export const Heading = {
  args: {
    as: "h1",
    children: "Hello World",
    fontSize: "4xl",
    color: "gray",
  },
};
