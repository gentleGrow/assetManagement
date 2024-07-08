import run from "@gaemi-school/esbuild-config";
import pkg from "./package.json" assert { type: "json" };
//const dev = process.env.NODE_ENV === "development";

run({pkg,})