import { SegmentedButton, SegmentedButtonGroup } from "@/shared";
import type { Meta, StoryObj } from "@storybook/react";

const meta: Meta<typeof SegmentedButtonGroup> = {
  title: "React Components/SegmentedButtonGroup",
  component: SegmentedButtonGroup,
  parameters: {
    layout: "centered",
  },
};

export default meta;
type Story = StoryObj<typeof SegmentedButtonGroup>;

export const Default: Story = {
  render: () => (
    <SegmentedButtonGroup>
      <SegmentedButton>계좌별</SegmentedButton>
      <SegmentedButton>종목별</SegmentedButton>
      <SegmentedButton>유형별</SegmentedButton>
    </SegmentedButtonGroup>
  ),
};
