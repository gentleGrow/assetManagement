import { PortfolioItem } from "@/shared";
import PortfolioCarousel from "../../../shared/ui/PortfolioCarousel";

const OPTIONS = { slidesToScroll: "auto" };
export default function RichPortfolioGallery({ data }: { data: any[] }) {
  const carouselItems = data.map((item, index) => (
    <PortfolioItem
      item={item}
      key={index}
      chartName="포트폴리오 구경하기"
      isRichPortfolio={true}
    />
  ));

  return <PortfolioCarousel slides={carouselItems} options={OPTIONS} />;
}
