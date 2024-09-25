import type { Meta, StoryObj } from "@storybook/react";
import { MenuItem } from "@/widgets";
import "../../app/globals.css";

const meta: Meta<typeof MenuItem> = {
  title: "React Components/GNB/MenuItem",
  component: MenuItem,
  parameters: {
    layout: "centered",
  },
};

export default meta;

type Story = StoryObj<typeof MenuItem>;

export const Default: Story = {
  args: {
    name: "menu1",
    href: "/",
    isSelected: false,
    isHovered: false,
  },
};

export const Hover: Story = {
  args: {
    ...Default.args,
    isHovered: true,
  },
};

export const Selected: Story = {
  args: {
    ...Default.args,
    isSelected: true,
  },
};
