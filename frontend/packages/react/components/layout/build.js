import run from "@gaemi-school/esbuild-config";
import pkg from "./package.json" assert { type: "json" };
//const dev = process.env.NODE_ENV === "development";
import {vanillaExtractPlugin} from '@vanilla-extract/esbuild-plugin';

const config = {
  plugins: [vanillaExtractPlugin()],
}

run({pkg,config,});           