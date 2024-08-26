"use server";

import jwt, { JwtPayload } from "jsonwebtoken";
import { cookies } from "next/headers";

const validateTokenExpiry = async () => {
  try {
    const cookieStore = cookies();
    const accessToken: string | undefined =
      cookieStore.get("accessToken")?.value;
    if (!accessToken) return false;

    const payload: JwtPayload | null = jwt.decode(
      accessToken,
    ) as JwtPayload | null;
    if (!payload || typeof payload.exp !== "number") return false;

    const currentTime = Math.floor(Date.now() / 1000);
    if (currentTime < payload.exp) return true;

    const refreshToken: string | undefined =
      cookieStore.get("refreshToken")?.value;
    if (!refreshToken) return false;

    const response = await fetch("/api/auth/refresh", { method: "POST" });

    if (!response.ok) return false;

    return true;
  } catch (error) {
    console.error("Error validating token:", error);
    return false;
  }
};

export default validateTokenExpiry;
