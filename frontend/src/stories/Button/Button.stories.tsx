import React from "react";
import { Button } from "@/shared/ui/button/Button";
import { colors } from "@/shared/ui/themes/variables/colors/scale";
import { useButton } from "@/shared/ui/button/hooks/useButton";
import { useToggleButton } from "@/shared/ui/button/hooks/useToggleButton";
import { Text } from "@/shared/ui/layout/src";

export default {
  title: "React Components/Button",
  component: Button,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
  argTypes: {
    size: {
      options: ["xs", "sm", "md", "lg"],
      control: "select",
    },
    color: {
      options: Object.keys(colors),
      control: "select",
    },
    variant: {
      options: ["primary", "outline"],
      control: "select",
    },
  },
};

export const ButtonStory = {
  args: {
    // size: "lg",
    size: "md",
    children: "적용하기",
    variant: "primary",
    isDisabled: false,
    isLoading: false,
    // leftIcon: "😀",
  },
};

export const TextButtonStory = {
  render: () => {
    const { buttonProps } = useButton({
      elementType: "div",
      onClick: () => {
        console.log("ttt");
      },
    });

    return (
      <Text
        {...buttonProps}
        as="div"
        fontSize="md"
        color="green"
        style={{
          userSelect: "none",
          cursor: "pointer",
        }}
      >
        텍스트 버튼입니다.
      </Text>
    );
  },
};

export const ToggleButtonStory = {
  render: () => {
    const { buttonProps, isSelected } = useToggleButton(
      { elementType: "button" },
      false,
    );

    return (
      <Button
        {...buttonProps}
        variant={isSelected ? "solid" : "outline"}
        color="green"
      >
        {isSelected ? "😀" : "😂"}
      </Button>
    );
  },
};
