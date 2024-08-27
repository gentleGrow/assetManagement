"use server";
import { getGoogleOAuth2Client } from "@/shared";

const getGoogleOAuthUrl = () => {
  const client = getGoogleOAuth2Client();

  const authUrl = client.generateAuthUrl({
    access_type: "online",
    scope: ["openid"],
    prompt: "consent",
  });
  return authUrl;
};

export default getGoogleOAuthUrl;
