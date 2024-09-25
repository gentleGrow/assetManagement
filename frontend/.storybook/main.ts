import { VanillaExtractPlugin } from "@vanilla-extract/webpack-plugin";
import type { StorybookConfig } from "@storybook/nextjs";

const config: StorybookConfig = {
  stories: ["../src/**/*.mdx", "../src/**/*.stories.@(js|jsx|mjs|ts|tsx)"],
  addons: [
    "@storybook/addon-onboarding",
    "@storybook/addon-links",
    "@storybook/addon-essentials",
    "@chromatic-com/storybook",
    "@storybook/addon-interactions",
  ],
  framework: {
    name: "@storybook/nextjs",
    options: {},
  },
  staticDirs: ["../public"],
  webpackFinal: async (config) => {
    config.plugins!.push(new VanillaExtractPlugin());

    // Node.js 전용 모듈들을 브라우저 빌드에서 무시하도록 설정
    config.resolve = {
      ...config.resolve,
      fallback: {
        ...config.resolve?.fallback,
        child_process: false,
        net: false,
        tls: false,
        fs: false,
      },
    };

    return config;
  },
};

export default config;
