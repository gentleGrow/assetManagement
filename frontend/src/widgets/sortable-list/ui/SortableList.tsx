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
import SortableItem from "./SortableItem";

const SortableList = ({ filteredColumns, setFilteredColumns }) => {
  const sensors = useSensors(
    useSensor(PointerSensor),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    }),
  );

  // 드래그 종료 시 호출되는 함수
  const handleDragEnd = (event) => {
    const { active, over } = event;

    if (active.id !== over.id) {
      setFilteredColumns((columns) => {
        const oldIndex = columns.findIndex((item) => item.id === active.id);
        const newIndex = columns.findIndex((item) => item.id === over.id);
        return arrayMove(columns, oldIndex, newIndex);
      });
    }
  };

  // 체크박스 변경 시 호출되는 함수
  const handleChange = (id) => {
    setFilteredColumns((columns) =>
      columns.map((item) =>
        item.id === id ? { ...item, checked: !item.checked } : item,
      ),
    );
  };

  return (
    <div className="h-[228px] overflow-y-auto">
      <DndContext
        sensors={sensors}
        collisionDetection={closestCenter}
        onDragEnd={handleDragEnd}
      >
        <SortableContext items={filteredColumns} strategy={verticalListSortingStrategy}>
          {filteredColumns.map((item) => (
            <SortableItem
              key={item.id}
              id={item.id}
              label={item.label}
              checked={item.checked}
              required={item.required}
              onChange={() => handleChange(item.id)}
            />
          ))}
        </SortableContext>
      </DndContext>
    </div>
  );
};

export default SortableList;
