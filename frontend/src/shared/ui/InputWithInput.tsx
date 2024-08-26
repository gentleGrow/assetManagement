import Input, { InputProps } from "./Input";

export default function InputWithImage({
  props,
  children,
}: {
  props: InputProps;
  children: React.ReactNode;
}) {
  return (
    <div className="relative">
      <div className="absolute top-1/2 -translate-y-1/2 pl-[10px]">
        {children}
      </div>
      <Input {...props} withImage={true} />
    </div>
  );
}
