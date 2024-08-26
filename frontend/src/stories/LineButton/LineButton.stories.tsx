import type { Meta, StoryObj } from "@storybook/react";
import "../../app/globals.css";
import { LineButton } from "@/shared";

const meta: Meta<typeof LineButton> = {
  title: "React Components/LineButton",
  component: LineButton,
  parameters: {
    layout: "centered",
  },
};

export default meta;

type Story = StoryObj<typeof LineButton>;

export const Default: Story = {
  args: {
    title: "구글로 계속하기",
    children: (
      <svg
        width="20"
        height="20"
        viewBox="0 0 20 20"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d="M19.8215 10.2271C19.8215 9.51804 19.7578 8.83624 19.6393 8.18164H10.2004V12.0498H15.594C15.3617 13.2998 14.6557 14.3589 13.5943 15.068V17.5771H16.8332C18.7282 15.8362 19.8215 13.2725 19.8215 10.2271Z"
          fill="#4285F4"
        />
        <path
          d="M10.2005 20.0004C12.9064 20.0004 15.175 19.1049 16.8331 17.5777L13.5942 15.0686C12.6968 15.6686 11.5488 16.0231 10.2005 16.0231C7.59016 16.0231 5.38083 14.264 4.5927 11.9004H1.24448V14.4913C2.89358 17.7595 6.2828 20.0004 10.2005 20.0004Z"
          fill="#34A853"
        />
        <path
          d="M4.59266 11.9007C4.39222 11.3007 4.27837 10.6598 4.27837 10.0007C4.27837 9.34157 4.39222 8.70067 4.59266 8.10067V5.50977H1.24443C0.565744 6.85977 0.178497 8.38707 0.178497 10.0007C0.178497 11.6143 0.565744 13.1416 1.24443 14.4916L4.59266 11.9007Z"
          fill="#FBBC04"
        />
        <path
          d="M10.2005 3.9773C11.6718 3.9773 12.9929 4.4818 14.0316 5.4727L16.906 2.6045C15.1705 0.9909 12.9018 0 10.2005 0C6.2828 0 2.89358 2.2409 1.24448 5.5091L4.5927 8.1C5.38083 5.7364 7.59016 3.9773 10.2005 3.9773Z"
          fill="#E94235"
        />
      </svg>
    ),
  },
};

export const Hover: Story = {
  args: {
    ...Default.args,
    isHover: true,
  },
};

export const Disabled: Story = {
  args: {
    ...Default.args,
    isDisabled: true,
  },
};
