"use client";
import { LineButton } from "@/shared";

export default function NaverLoginButton() {
  const loginNaver = () => {
    window.location.href = "/api/auth/naver";
  };
  return (
    <LineButton
      title="네이버로 계속하기"
      props={{
        className: "bg-[#03C75A] text-white border-[#03C75A]",
        onClick: () => loginNaver(),
      }}
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
    </LineButton>
  );
}
