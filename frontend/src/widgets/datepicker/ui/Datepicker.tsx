import { useState, forwardRef, useEffect } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { ko } from "date-fns/locale";
import { Button } from "@/shared/ui/button/Button";
import Image from "next/image";
import styles from "./styles.module.css";
import { format } from "date-fns";

interface CustomInputProps {
  value?: string;
  onClick?: () => void;
}

const CustomInput = forwardRef<HTMLInputElement, CustomInputProps>(
  ({ value, onClick }, ref) => {
    return (
      <div className="flex w-full cursor-pointer rounded-md border px-3 py-2">
        <Image
          src="/images/calendar.svg"
          alt="calendar"
          width={24}
          height={24}
          className="flex-shrink-0"
        />
        <input
          type="text"
          ref={ref}
          onClick={onClick}
          value={value}
          className="focus:ring-none flex-grow cursor-pointer pl-3 focus:outline-none box-border min-w-0"
          placeholder="YYYY.MM.DD"
          readOnly
        />
      </div>
    );
  },
);

// forwardRef로 생성한 컴포넌트는 디스플레이 이름을 설정해 주면 디버깅 시 도움이 됩니다.
CustomInput.displayName = "CustomInput";

const DatepickerComponent = ({
  value,
  onChange,
}: {
  value?: any;
  onChange?: (value: any) => void;
}) => {
  const [selectedDate, setSelectedDate] = useState<Date | null>(null);
  const [showMonthPicker, setShowMonthPicker] = useState(false);

  useEffect(() => {
    setSelectedDate(value ? new Date(value) : null);
  }, [value]);

  const handleDateChange = (date: Date | null) => {
    setSelectedDate(date);
    if (onChange) {
      if (!date) return "";
      console.log('format(date, "yyyy-MM-dd"', format(date, "yyyy-MM-dd"));

      onChange(format(date, "yyyy-MM-dd"));
    }
  };

  const handleYearMonthClick = () => {
    setShowMonthPicker(!showMonthPicker);
  };

  const handleCalendarClose = () => {
    setShowMonthPicker(false);
  };

  const isToday = (date: Date) => {
    const today = new Date();
    return (
      date.getDate() === today.getDate() &&
      date.getMonth() === today.getMonth() &&
      date.getFullYear() === today.getFullYear()
    );
  };

  const renderDayContents = (day: number, date: Date) => {
    if (isToday(date)) {
      return (
        <div className="relative flex items-center justify-center">
          <div className="absolute -top-0 left-1/2 h-[4px] w-[4px] -translate-x-1/2 rounded-full bg-green-60" />
          <span>{day}</span>
        </div>
      );
    }

    return (
      <div className="relative flex items-center justify-center">
        <span>{day}</span>
      </div>
    );
  };

  const renderMonthContent = (
    month: number,
    shortMonthText: string,
    fullMonthText: string,
    day: Date,
  ) => {
    return (
      <div className="flex w-full items-center justify-center">
        <div className="flex h-[36px] w-[36px] items-center justify-center rounded-full">
          <span>{month + 1}</span>
        </div>
      </div>
    );
  };

  return (
    <div className={`relative w-full ${styles.customDatepicker}`}>
      <DatePicker
        className={styles.customDatepicker}
        selected={selectedDate}
        onChange={
          showMonthPicker ? () => setShowMonthPicker(false) : handleDateChange
        }
        locale={ko}
        dateFormat={"yyyy.MM.dd"}
        showMonthYearPicker={showMonthPicker}
        popperPlacement="bottom"
        customInput={
          <CustomInput
            value={selectedDate ? selectedDate.toLocaleDateString() : ""}
          />
        }
        showPopperArrow={false}
        onCalendarClose={handleCalendarClose}
        shouldCloseOnSelect={showMonthPicker ? false : true}
        disabledKeyboardNavigation
        renderDayContents={renderDayContents}
        renderMonthContent={renderMonthContent}
        renderCustomHeader={({
          date,
          decreaseMonth,
          increaseMonth,
          decreaseYear,
          increaseYear,
          prevMonthButtonDisabled,
          nextMonthButtonDisabled,
        }) => (
          <div className="flex items-center justify-between bg-white pb-[10px]">
            <Button
              variant="icon"
              size="icon"
              leftIcon={
                <Image
                  src="/images/arrow_left.svg"
                  alt="left arrow button"
                  width={20}
                  height={20}
                />
              }
              onClick={showMonthPicker ? decreaseYear : decreaseMonth}
              disabled={prevMonthButtonDisabled}
            />
            <button
              type="button"
              className="rounded-[6px] px-[12px] py-[7px] text-xs font-semibold text-gray-100 hover:bg-gray-10"
              onClick={handleYearMonthClick}
            >
              {`${date.getFullYear()}. ${String(date.getMonth() + 1).padStart(2, "0")}`}
            </button>
            <Button
              variant="icon"
              size="icon"
              leftIcon={
                <Image
                  src="/images/arrow_right.svg"
                  alt="right arrow button"
                  width={20}
                  height={20}
                />
              }
              onClick={showMonthPicker ? increaseYear : increaseMonth}
              disabled={nextMonthButtonDisabled}
            />
          </div>
        )}
      />
    </div>
  );
};

export default DatepickerComponent;
