"use server";
import { OutlineButton } from "@/shared";
import Link from "next/link";

export default async function KakaoLoginButton() {
  return (
    <Link
      href={`https://kauth.kakao.com/oauth/authorize?client_id=${process.env.KAKAO_CLIENT_ID}&redirect_uri=${process.env.KAKAO_REDIRECT_URI}&response_type=code&scope=openid`}
    >
      <OutlineButton
        title="카카오로 계속하기"
        className="border-[#FEE500] bg-[#FEE500]"
      >
        <svg
          width="20"
          height="20"
          viewBox="0 0 20 20"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            fill-rule="evenodd"
            clip-rule="evenodd"
            d="M9.75 0.62085C4.72667 0.62085 0.25 4.0964 0.25 8.38363C0.25 11.0492 1.98167 13.4003 4.61833 14.7981L3.50889 18.8703C3.41056 19.2308 3.82056 19.5175 4.135 19.3086L8.99833 16.0836C9.40833 16.1231 9.82556 16.1464 9.75 16.1464C15.7728 16.1464 19.75 12.6703 19.75 8.38363C19.75 4.0964 15.7728 0.62085 9.75 0.62085Z"
            fill="black"
            fill-opacity="0.9"
          />
        </svg>
      </OutlineButton>
    </Link>
  );
}
