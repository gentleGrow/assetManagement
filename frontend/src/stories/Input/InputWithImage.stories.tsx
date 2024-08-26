import type { Meta, StoryObj } from "@storybook/react";
import "../../app/globals.css";
import { InputWithImage } from "@/shared";

const meta: Meta<typeof InputWithImage> = {
  title: "React Components/InputWithImage",
  component: InputWithImage,
  parameters: {
    layout: "centered",
  },
};

export default meta;

type Story = StoryObj<typeof InputWithImage>;

export const Default: Story = {
  args: {
    props: {
      placeholder: "검색어를 입력해 주세요.",
      type: "text",
    },
    children: (
      <svg
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <rect width="24" height="24" fill="white" />
        <path
          d="M16 16L19 19"
          stroke="#5D646E"
          strokeWidth="1.5"
          strokeLinecap="round"
        />
        <circle
          cx="11.5"
          cy="11.5"
          r="5.75"
          stroke="#5D646E"
          strokeWidth="1.5"
        />
      </svg>
    ),
  },
};
