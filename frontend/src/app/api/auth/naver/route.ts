import { NextResponse } from "next/server";

export function GET() {
  const state = Math.random().toString(36).substring(7);
  const naverAuthUrl = `https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id=${process.env.NAVER_CLIENT_ID}&redirect_uri=${process.env.NAVER_REDIRECT_URI}&state=${state}`;

  return NextResponse.redirect(naverAuthUrl);
}
