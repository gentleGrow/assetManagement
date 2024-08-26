"use server";

import { cookies } from "next/headers";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants/cookie";

const setJWTCookie = (accessToken: string, refreshToken: string) => {
  const cookieStore = cookies();
  cookieStore.set(ACCESS_TOKEN, accessToken, {
    sameSite: "none",
    httpOnly: true,
    secure: true,
  });
  cookieStore.set(REFRESH_TOKEN, refreshToken, {
    sameSite: "none",
    httpOnly: true,
    secure: true,
  });
};
export default setJWTCookie;
