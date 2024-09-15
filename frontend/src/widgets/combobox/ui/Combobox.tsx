"use client";

import {
  Combobox,
  ComboboxButton,
  ComboboxInput,
  ComboboxOption,
  ComboboxOptions,
} from "@headlessui/react";
import clsx from "clsx";
import { useState, useEffect } from "react";
import { saveStocks, searchStocks } from "@/shared/lib/indexedDB";

export default function Example({ stocks }) {
  const [query, setQuery] = useState("");
  const [selected, setSelected] = useState({ code: "1", name: "Tom Cook" });
  const [results, setResults] = useState([]);

  const handleSearch = async (query) => {
    setQuery(query);
    if (query) {
      const searchResults: any = await searchStocks(query);
      setResults(searchResults);
    } else {
      setResults([]);
    }
  };

  useEffect(() => {
    saveStocks(stocks);
  }, [stocks]);

  return (
    <Combobox
      value={selected}
      onChange={(value: { code: string; name: string }) => setSelected(value)}
      onClose={() => setQuery("")}
    >
      <div className="relative">
        <ComboboxInput
          className={clsx(
            "w-full rounded-lg border-none bg-white px-2.5 py-1.5 text-sm/6 text-gray-90 ring-0 ring-inset",
            "focus:outline-none data-[focus]:ring-1 data-[focus]:ring-green-60",
          )}
          displayValue={(result: { code: string; name: string }) =>
            result?.name
          }
          onChange={(event) => handleSearch(event.target.value)}
        />
        <ComboboxButton className="group absolute inset-y-0 right-0 px-2.5">
          {/* <ChevronDownIcon className="size-4 fill-white/60 group-data-[hover]:fill-white" /> */}
        </ComboboxButton>
      </div>

      <ComboboxOptions
        anchor="bottom"
        transition
        className={clsx(
          "bg-white text-gray-900[--anchor-gap:var(--spacing-1)] w-[var(--input-width)] rounded-xl border border-gray-20 bg-white/5 px-2 py-1 empty:invisible",
          "transition duration-100 ease-in data-[leave]:data-[closed]:opacity-0",
        )}
      >
        {results.map((result: { code: string; name: string }) => (
          <ComboboxOption
            key={result.code}
            value={result}
            className="bg-white group flex cursor-default select-none items-center gap-2 border-green-60 px-2 py-1 data-[focus]:border-l-2 data-[focus]:bg-gray-5"
          >
            {/* <CheckIcon className="invisible size-4 fill-white group-data-[selected]:visible" /> */}
            <div className="text-sm/6 text-gray-90">{result.name}</div>
          </ComboboxOption>
        ))}
      </ComboboxOptions>
    </Combobox>
  );
}
