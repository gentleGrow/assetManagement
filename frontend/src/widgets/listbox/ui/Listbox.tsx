"use client";

import { useState } from "react";
import {
  Label,
  Listbox,
  ListboxButton,
  ListboxOption,
  ListboxOptions,
} from "@headlessui/react";

export default function ListboxComponent({
  options,
  iconPath,
}: {
  options: { id: string; name: string }[];
  iconPath?: string;
}) {
  const [selected, setSelected] = useState(options?.[0]);

  return (
    <Listbox value={selected} onChange={setSelected}>
      <Label className="block text-sm font-medium leading-6 text-gray-900">
        Assigned to
      </Label>
      <div className="relative mt-2">
        <ListboxButton className="relative w-full cursor-default rounded-md bg-white px-2.5 py-1.5 text-left text-gray-900 shadow-sm ring-0 ring-inset ring-gray-300 focus:outline-none focus:ring-1 focus:ring-green-60 sm:text-sm sm:leading-6">
          <div className="relative flex h-7 items-center rounded-[100px] border border-gray-20 px-2 py-1">
            <span className="flex items-center">
              {iconPath && (
                <img
                  src={iconPath}
                  alt="Securities Icon"
                  className="h-4 w-4 flex-shrink-0 rounded-full"
                />
              )}

              <span className="ml-1 block truncate">{selected?.name}</span>
            </span>
            <span className="pointer-events-none absolute inset-y-0 right-0 ml-3 flex items-center pr-2">
              <img
                src="/images/arrow_down.svg"
                alt="Securities Icon"
                aria-hidden="true"
                className="h-4 w-4 flex-shrink-0 text-gray-400"
              />
            </span>
          </div>
        </ListboxButton>

        <ListboxOptions
          transition
          className="absolute z-10 mt-1 flex max-h-56 w-full flex-col gap-1.5 overflow-auto rounded-md bg-white py-2 pl-2 pr-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none data-[closed]:data-[leave]:opacity-0 data-[leave]:transition data-[leave]:duration-100 data-[leave]:ease-in sm:text-sm"
        >
          {options?.map((option: { id: string; name: string }) => (
            <ListboxOption
              key={option.id}
              value={option}
              className="group relative cursor-default select-none border-green-60 px-2 py-1 text-gray-900 data-[focus]:border-l-2 data-[focus]:bg-gray-5"
            >
              <div className="flex h-7 items-center rounded-[100px] border border-gray-20 px-2 py-1">
                {iconPath && (
                  <img
                    src={iconPath}
                    alt="Securities Icon"
                    className="h-4 w-4 flex-shrink-0 rounded-full"
                  />
                )}

                <span className="ml-1 block truncate text-sm font-normal text-gray-90 group-data-[selected]:font-semibold">
                  {option.name}
                </span>
              </div>
            </ListboxOption>
          ))}
        </ListboxOptions>
      </div>
    </Listbox>
  );
}
