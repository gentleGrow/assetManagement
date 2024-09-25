"use client";
import React from "react";

import useEmblaCarousel from "embla-carousel-react";
import { ArrowButtons } from "@/shared";
import { usePrevNextButtons } from "../hooks/useCarouselPrevNextButtons";

const PortfolioCarousel = (props) => {
  const { slides, options } = props;
  const [emblaRef, emblaApi] = useEmblaCarousel(options);

  const {
    prevBtnDisabled,
    nextBtnDisabled,
    onPrevButtonClick,
    onNextButtonClick,
  } = usePrevNextButtons(emblaApi);

  return (
    <section className="embla">
      <div className="embla__viewport" ref={emblaRef}>
        <div className="embla__container">
          {slides.map((item, index) => (
            <div className="embla__slide" key={index}>
              {item}
            </div>
          ))}
        </div>
      </div>

      <div className="absolute right-[16px] top-[16px] mobile:hidden">
        <ArrowButtons
          onLeftClick={onPrevButtonClick}
          onRightClick={onNextButtonClick}
          leftDisabled={prevBtnDisabled}
          rightDisabled={nextBtnDisabled}
        />
      </div>
    </section>
  );
};

export default PortfolioCarousel;
