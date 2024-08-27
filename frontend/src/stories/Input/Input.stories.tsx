import type { Meta, StoryObj } from "@storybook/react";
import "../../app/globals.css";
import { Input } from "@/shared";

const meta: Meta<typeof Input> = {
  title: "React Components/Input",
  component: Input,
  parameters: {
    layout: "centered",
  },
};

export default meta;

type Story = StoryObj<typeof Input>;

export const Default: Story = {
  args: {
    placeholder: "수량을 입력해 주세요.",
    type: "text",
  },
};

export const Hover: Story = {
  args: {
    ...Default.args,
    isHovered: true,
    value: "input / hover 입니다.",
  },
};
export const Selected: Story = {
  args: {
    ...Default.args,
    isSelected: true,
    value: "input / typing 중입니다.",
  },
};
export const Done: Story = {
  args: {
    ...Default.args,
    value: "input / 입력 완료한 상태입니다.",
  },
};

export const Disable: Story = {
  args: {
    ...Default.args,
    isDisabled: true,
    value: "input / disabled 입니다.",
  },
};
