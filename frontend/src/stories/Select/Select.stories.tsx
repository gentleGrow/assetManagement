import "@/shared/ui/select/style.css";
import { Select } from "@/shared/ui/select";
import React from "react";

import "@/shared/ui/layout/style.css";


export default {
  title: "React Components/Select",
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
};

export const SelectStory = {
  render: () => <Select>
    <option value="1">1</option>
    <option value="2">2</option>
  </Select>,
};