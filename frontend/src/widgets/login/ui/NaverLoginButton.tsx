"use server";
import { OutlineButton } from "@/shared";
import Link from "next/link";

export default async function NaverLoginButton() {
  const state = Math.random().toString(36).substring(7);
  return (
    <Link
      href={`https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id=${process.env.NAVER_CLIENT_ID}&redirect_uri=${process.env.NAVER_REDIRECT_URI}&state=${state}`}
    >
      <OutlineButton
        title="네이버로 계속하기"
        className="border-[#03C75A] bg-[#03C75A] text-white"
      >
        <svg
          width="20"
          height="20"
          viewBox="0 0 20 20"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M13.035 10.59L6.72669 1.57019H1.50024V18.4297H6.97958V9.40986L13.2738 18.4297H18.5002V1.57019H13.035V10.59Z"
            fill="white"
          />
        </svg>
      </OutlineButton>
    </Link>
  );
}
