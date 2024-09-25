import { createVanillaExtractPlugin } from "@vanilla-extract/next-plugin";

const withVanillaExtract = createVanillaExtractPlugin();

/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: "/api/v1/:path*", // 프록시를 사용할 경로
        destination: "http://api.gaemischool.com:8000/api/v1/:path*", // 실제 API 서버 주소
      },
    ];
  },
};

export default withVanillaExtract(nextConfig);
