const {build} = require('esbuild');

const run = ({
  entryPoints = ['src/index.ts'], pkg, config = {},
}) => {
  const dev = process.argv.includes("--dev"); // script에서 dev가 들어왔을 때
const minify = !dev; // minify 실행하지 않음 (빠른 개발환경을 위해)

// 코드가 변경되었을 때 바로 빌드하도록 watch 옵션 추가
const watch = process.argv.includes("--watch");

// 라이브러리를 만드는 것이므로 외부 의존성을 모두 external로 설정 (번들링 될 필요 없음)
const external = Object.keys(
  { ...pkg.dependencies, ...pkg.peerDependencies } || {}
);
const baseConfig = {
  entryPoints,
  bundle: true,
  minify,
  sourcemap: true,
  outdir: "dist", 
  target: "es2019",
  external,
  ...config
};

const buildOptions = [
  {  
    ...baseConfig,
    format: "esm",
  },
  {
    ...baseConfig,
    format: "cjs",
    outExtension: { ".js": ".cjs" },
  },
];

async function buildAll() {
  try {
    await Promise.all(buildOptions.map((options) => build(options)));
    console.log("Build succeeded");
  } catch (error) {
    console.error("Build failed:", error);
    process.exit(1);
  }
}

if (watch) {
  buildOptions.forEach((options) => {
    build({
      ...options,
      watch: {
        onRebuild(error, result) {
          if (error) {
            console.error("Watch build failed:", error);
          } else {
            console.log("Watch build succeeded:", result);
          }
        },
      },
    });
  });
} else {
  buildAll();
}
}

module.exports = run;