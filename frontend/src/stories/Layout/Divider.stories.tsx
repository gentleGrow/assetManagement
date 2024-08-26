import { Divider as _Divider, Box } from "@/shared/ui/layout/src";
import { colors } from "@/shared/ui/themes/variables/colors/scale";

export default {
  title: "React Components/Layout/Divider",
  component: _Divider,
  decorators: [
    (Story: any) => (
      <Box padding={3} style={{ width: "300px", height: "300px" }}>
        <Story />
      </Box>
    ),
  ],
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
  argTypes: {
    orientation: {
      options: ["horizontal", "vertical"],
      control: "select",
    },
    variant: {
      options: ["solid", "dashed"],
      control: "select",
    },
    color: {
      options: Object.keys(colors),
      control: "select",
    },
  },
};

export const Divider = {
  args: {
    color: "gray",
    size: 1,
    variant: "solid",
    orientation: "horizontal",
  },
};
