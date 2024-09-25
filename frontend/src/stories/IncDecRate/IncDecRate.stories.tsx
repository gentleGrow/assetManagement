import type { Meta, StoryObj } from "@storybook/react";
import "../../app/globals.css";
import { IncDecRate } from "@/shared";

const meta: Meta<typeof IncDecRate> = {
  title: "React Components/IncDecRate",
  component: IncDecRate,
  parameters: {
    layout: "centered",
  },
};

export default meta;

type Story = StoryObj<typeof IncDecRate>;

export const Zero: Story = {
  args: {
    rate: 0,
  },
};

export const Increment: Story = {
  args: {
    rate: 10,
  },
};

export const Decrement: Story = {
  args: {
    rate: -10,
  },
};
