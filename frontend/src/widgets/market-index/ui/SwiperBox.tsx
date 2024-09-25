"use client";
import { Swiper, SwiperSlide } from "swiper/react";
import { Autoplay, FreeMode } from "swiper/modules";
import "swiper/css";
import styles from "./styles.module.css";

export default function SwiperBox({ items }: { items: any[] }) {
  return (
    <Swiper
      className={styles.swiperWrapper}
      modules={[Autoplay, FreeMode]}
      autoplay={{
        delay: 0,
        stopOnLastSlide: false,
        pauseOnMouseEnter: false,
        disableOnInteraction: false,
      }}
      loop={true}
      speed={5000}
      slidesPerView="auto"
      centeredSlides={false}
      grabCursor={true}
    >
      {items.map((item, index) => (
        <SwiperSlide key={index}>{item}</SwiperSlide>
      ))}
    </Swiper>
  );
}
