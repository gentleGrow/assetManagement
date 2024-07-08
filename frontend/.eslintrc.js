module.exports = {
  env: {
    browser: true,
    es2021: true,
    node: true,
  },
  root: true,
  parser: "@typescript-eslint/parser",
  parserOptions: {
    project: "./tsconfig.eslint.json",
tsconfigRootDir: __dirname,
  },
  "extends": [
    "eslint:recommended",
    "plugin:react/recommended",
    "plugin:storybook/recommended",
    "prettier",
  ],
  "plugins": [
    "react",
    "@typescript-eslint",
    "react-hooks",
    "jsx-ally"
  ],
  "rules": {
    "react-hooks/rules-of-hooks": "error",
    "react-hooks/exhaustive-deps": "warn",
    "react/react-in-jsx-scope": "off", //'import React' 미사용시 오류 억제
"comma-dangle": "off",
"no-empty-function": "off",
"@typescript-eslint/no-empty-function": ["off"], // namespace 사용 가능
"@typescript-eslint/no-unused-vars": ["error", {
  argsIgnorePattern: "^_",
}],
"storybook/prefer-pascal-case": "off",
  },
  overrides: [
    {
      files: ["*.ts", "*.tsx"],
      rules: {
        "no-undef": "off",
      },
    },
  ],
  "ignorePatterns": ["**/dist/**/*", ".eslintrc.js"],
  "settings": {
    "import/resolver": {
  typescript: {},
    },
  },
};