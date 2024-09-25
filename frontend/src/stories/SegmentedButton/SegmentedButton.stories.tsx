import type { Meta, StoryObj } from "@storybook/react";
import "../../app/globals.css";
import { SegmentedButton } from "@/shared";

const meta: Meta<typeof SegmentedButton> = {
  title: "React Components/SegmentedButtonGroup/SegmentedButton",
  component: SegmentedButton,
  parameters: {
    layout: "centered",
    backgrounds: {
      values: [{ name: "gray", value: "#F7F8FA" }],
    },
  },
  args: {
    children: "텍스트",
  },
};

export default meta;

type Story = StoryObj<typeof SegmentedButton>;

export const Default: Story = {
  args: {},
};

export const Hover: Story = {
  args: { isHover: true },
};

export const Selected: Story = {
  args: { isSelected: true },
  parameters: {
    backgrounds: { default: "gray" },
  },
};
