import { NextResponse } from "next/server";

export function GET() {
  const kakaoAuthUrl = `https://kauth.kakao.com/oauth/authorize?client_id=${process.env.KAKAO_CLIENT_ID}&redirect_uri=${process.env.KAKAO_REDIRECT_URI}&response_type=code&scope=openid`;
  return NextResponse.redirect(kakaoAuthUrl);
}
