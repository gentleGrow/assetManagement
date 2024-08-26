import {
  getGoogleOAuth2Client,
  RESPONSE_STATUS,
  SERVICE_SERVER_URL,
} from "@/shared";
import setJWTCookie from "@/shared/utils/setJWTCookie";
import { NextResponse } from "next/server";

export async function GET(req: Request) {
  const client = getGoogleOAuth2Client();
  const requestUrl = new URL(req.url);
  const authenticationCode = requestUrl.searchParams.get("code");

  if (!authenticationCode) {
    return NextResponse.json(
      { error: "Google 계정 인증코드 발급이 실패했습니다." },
      { status: RESPONSE_STATUS.BAD_REQUEST },
    );
  }

  try {
    const { tokens } = await client.getToken(authenticationCode);
    const idToken = tokens.id_token;

    if (!idToken) {
      return NextResponse.json(
        { error: "Google로부터 ID 토큰을 가져오는 작업을 실패했습니다." },
        { status: RESPONSE_STATUS.INTERNAL_SERVER_ERROR },
      );
    }

    let jwtResponse;
    try {
      jwtResponse = await fetch(`${SERVICE_SERVER_URL}/api/auth/v1/google`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id_token: idToken }),
      });
    } catch (fetchError) {
      return NextResponse.json(
        { error: "서비스 서버와의 연결에서 문제가 발생했습니다." },
        { status: RESPONSE_STATUS.INTERNAL_SERVER_ERROR },
      );
    }

    if (!jwtResponse.ok) {
      const tokenResponseErrorText = await jwtResponse.text();
      return NextResponse.json(
        {
          error: `서비스 서버에서 오류가 발생했습니다.: ${tokenResponseErrorText}`,
        },
        { status: jwtResponse.status },
      );
    }

    const jwtData = await jwtResponse.json();
    setJWTCookie(jwtData.access_token, jwtData.refresh_token);
    const redirectUrl = new URL("/", requestUrl);
    return NextResponse.redirect(redirectUrl);
  } catch (error) {
    return NextResponse.json(
      { error: "Google 로그인이 알 수 없는 이유로 실패했습니다." },
      { status: RESPONSE_STATUS.INTERNAL_SERVER_ERROR },
    );
  }
}
