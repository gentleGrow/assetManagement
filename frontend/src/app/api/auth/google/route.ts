import { getGoogleOAuth2Client } from "@/shared";
import { NextResponse } from "next/server";

export async function GET() {
  const client = getGoogleOAuth2Client();

  const authUrl = client.generateAuthUrl({
    access_type: "online",
    scope: ["openid"],
    prompt: "consent",
  });
  return NextResponse.redirect(authUrl);
}
