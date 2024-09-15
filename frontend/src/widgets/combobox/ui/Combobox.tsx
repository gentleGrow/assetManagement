"use client";

import {
  Combobox,
  ComboboxButton,
  ComboboxInput,
  ComboboxOption,
  ComboboxOptions,
} from "@headlessui/react";
import clsx from "clsx";
import { useState } from "react";

const people = [
  { id: "1", name: "Tom Cook" },
  { id: "2", name: "Wade Cooper" },
  { id: "3", name: "Tanya Fox" },
  { id: "4", name: "Arlene Mccoy" },
  { id: "5", name: "Devon Webb" },
];

export default function Example() {
  const [query, setQuery] = useState("");
  const [selected, setSelected] = useState(people[1]);

  const filteredPeople =
    query === ""
      ? people
      : people.filter((person) => {
          return person.name.toLowerCase().includes(query.toLowerCase());
        });

  return (
    <Combobox
      value={selected}
      onChange={(value: { id: string; name: string }) => setSelected(value)}
      onClose={() => setQuery("")}
    >
      <div className="relative">
        <ComboboxInput
          className={clsx(
            "w-full rounded-lg border-none bg-white px-2.5 py-1.5 text-sm/6 text-gray-90 ring-0 ring-inset",
            "focus:outline-none data-[focus]:ring-1 data-[focus]:ring-green-60",
          )}
          displayValue={(person: { id: string; name: string }) => person?.name}
          onChange={(event) => setQuery(event.target.value)}
        />
        <ComboboxButton className="group absolute inset-y-0 right-0 px-2.5">
          {/* <ChevronDownIcon className="size-4 fill-white/60 group-data-[hover]:fill-white" /> */}
        </ComboboxButton>
      </div>

      <ComboboxOptions
        anchor="bottom"
        transition
        className={clsx(
          "text-gray-900[--anchor-gap:var(--spacing-1)] w-[var(--input-width)] rounded-xl border border-gray-20 bg-white/5 px-2 py-1 empty:invisible",
          "transition duration-100 ease-in data-[leave]:data-[closed]:opacity-0",
        )}
      >
        {filteredPeople.map((person) => (
          <ComboboxOption
            key={person.id}
            value={person}
            className="group flex cursor-default select-none items-center gap-2 border-green-60 px-2 py-1 data-[focus]:border-l-2 data-[focus]:bg-gray-5"
          >
            {/* <CheckIcon className="invisible size-4 fill-white group-data-[selected]:visible" /> */}
            <div className="text-sm/6 text-gray-90">{person.name}</div>
          </ComboboxOption>
        ))}
      </ComboboxOptions>
    </Combobox>
  );
}
