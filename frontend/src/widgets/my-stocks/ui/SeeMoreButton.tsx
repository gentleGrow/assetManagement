import Image from "next/image";
import Link from "next/link";

export default function SeeMoreButton({ href }) {
  return (
    <Link href={href} className="flex items-center text-body-4">
      전체보기
      <Image
        src={"/images/right-arrow.svg"}
        width={16}
        height={16}
        alt="right arrow"
      />
    </Link>
  );
}
