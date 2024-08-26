import { Heading } from "@/shared";

export default function MenuName({
  name,
  isHovered = false,
}: {
  name: string;
  isHovered?: boolean;
}) {
  return (
    <Heading
      as="h4"
      fontSize="sm"
      className={`${isHovered && "text-gray-60"} text-gray-100 hover:text-gray-60`}
    >
      {name}
    </Heading>
  );
}
