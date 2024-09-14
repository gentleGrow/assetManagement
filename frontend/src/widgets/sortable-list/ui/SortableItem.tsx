// components/SortableList.js
"use client";
import React, { useState } from "react";
import {
  DndContext,
  closestCenter,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
} from "@dnd-kit/core";
import {
  arrayMove,
  SortableContext,
  sortableKeyboardCoordinates,
  useSortable,
  verticalListSortingStrategy,
} from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";

// 각 아이템 컴포넌트
const SortableItem = ({ id, label, checked, onChange }) => {
  const { attributes, listeners, setNodeRef, transform, transition } =
    useSortable({ id });

  // 아이템의 스타일 설정
  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    padding: "8px",
    margin: "4px 0",
    display: "flex",
    alignItems: "center",
    background: "#f0f0f0",
    borderRadius: "4px",
    cursor: "grab",
  };

  return (
    <div ref={setNodeRef} style={style}>
      <input type="checkbox" checked={checked} onChange={onChange} />
      <span style={{ marginLeft: "8px", flex: 1 }}>{label}</span>
      <span style={{ cursor: "grab" }} {...attributes} {...listeners}>
        ⋮
      </span>
    </div>
  );
};

export default SortableItem;
