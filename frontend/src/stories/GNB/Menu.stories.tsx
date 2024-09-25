import type { Meta, StoryObj } from "@storybook/react";
import { Menu } from "@/widgets";
import "../../app/globals.css";

const meta: Meta<typeof Menu> = {
  title: "React Components/GNB/Menu",
  component: Menu,
  parameters: {
    layout: "centered",
  },
};

export default meta;

type Story = StoryObj<typeof Menu>;

export const Default: Story = {
  args: {},
};

export const selectedItem: Story = {
  args: { selectedItem: "홈" },
};
