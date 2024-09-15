// components/SortableList.js
"use client";
import React, { useState } from "react";
import Image from "next/image";

import { useSortable } from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";
import Checkbox from "@/shared/ui/checkbox/Checkbox";

const SortableItem = ({ id, label, checked, onChange }) => {
  const { attributes, listeners, setNodeRef, transform, transition } =
    useSortable({ id });

  // 아이템의 스타일 설정
  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  };

  return (
    <div ref={setNodeRef} style={style} className="flex items-center space-y-1">
      <Checkbox label={label} checked={checked} onChange={onChange} />
      <Image
        src="/images/drag.svg"
        alt="Icon"
        width={24} // 원하는 너비
        height={24} // 원하는 높이
        style={{ cursor: "grab" }}
        {...attributes}
        {...listeners}
      />
    </div>
  );
};

export default SortableItem;
