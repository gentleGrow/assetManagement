import { faker } from "@faker-js/faker";

export type Person = {
  firstName: string;
  lastName: string;
  age: number;
  visits: number;
  progress: number;
  status: "relationship" | "complicated" | "single";
  subRows?: Person[];
};

const range = (len: number) => {
  const arr: number[] = [];
  for (let i = 0; i < len; i++) {
    arr.push(i);
  }
  return arr;
};

const newPerson = (): Person => {
  return {
    firstName: faker.person.firstName(),
    lastName: faker.person.lastName(),
    age: faker.number.int(40),
    visits: faker.number.int(1000),
    progress: faker.number.int(100),
    status: faker.helpers.shuffle<Person["status"]>([
      "relationship",
      "complicated",
      "single",
    ])[0]!,
  };
};

export function makeData(...lens: number[]) {
  const makeDataLevel = (depth = 0): Person[] => {
    const len = lens[depth]!;
    return range(len).map((d): Person => {
      return {
        ...newPerson(),
        subRows: lens[depth + 1] ? makeDataLevel(depth + 1) : undefined,
      };
    });
  };

  return makeDataLevel();
}

/* defaultData */
const defaultData: Person[] = [
  {
    firstName: "tanner",
    lastName: "linsley",
    age: 24,
    visits: 100,
    status: "relationship",
    progress: 50,
  },
  {
    firstName: "tandy",
    lastName: "miller",
    age: 40,
    visits: 40,
    status: "single",
    progress: 80,
  },
  {
    firstName: "joe",
    lastName: "dirte",
    age: 45,
    visits: 20,
    status: "complicated",
    progress: 10,
  },
];
