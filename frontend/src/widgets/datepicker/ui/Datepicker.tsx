import { useState, forwardRef } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { ko } from "date-fns/locale";

// 사용자 정의 입력창 컴포넌트
const CustomInput = forwardRef((props, ref: React.Ref<HTMLInputElement>) => {
  const { value, onClick } = props as { value: string; onClick: () => void }; // props에서 value와 onClick을 추출합니다.

  return (
    <input
      type="text"
      ref={ref}
      onClick={onClick}
      value={value}
      className="w-full cursor-pointer rounded-md border px-3 py-2"
      placeholder="YYYY.MM.DD"
      readOnly
    />
  );
});

// forwardRef로 생성한 컴포넌트는 디스플레이 이름을 설정해 주면 디버깅 시 도움이 됩니다.
CustomInput.displayName = "CustomInput";

const DatepickerComponent = () => {
  const [selectedDate, setSelectedDate] = useState<Date | null>(null);
  const [showMonthPicker, setShowMonthPicker] = useState(false);

  const handleDateChange = () => {
    setShowMonthPicker(false);
  };

  const handleYearMonthClick = () => {
    setShowMonthPicker(true);
  };

  const handleCalendarClose = () => {
    setShowMonthPicker(false);
  };

  return (
    <div className="relative">
      <DatePicker
        selected={selectedDate}
        onChange={
          showMonthPicker ? handleDateChange : (date) => setSelectedDate(date)
        }
        locale={ko}
        dateFormat={"yyyy.MM.dd"}
        showMonthYearPicker={showMonthPicker}
        popperPlacement="bottom"
        customInput={<CustomInput />}
        showPopperArrow={false}
        dayClassName={(date) =>
          date.getDate() === new Date().getDate()
            ? "bg-green-500 text-white rounded-full"
            : ""
        }
        onCalendarClose={handleCalendarClose}
        shouldCloseOnSelect={showMonthPicker ? false : true}
        renderCustomHeader={({
          date,
          decreaseMonth,
          increaseMonth,
          decreaseYear,
          increaseYear,
          prevMonthButtonDisabled,
          nextMonthButtonDisabled,
        }) => (
          <div className="flex items-center justify-between px-2 py-1">
            <button
              onClick={showMonthPicker ? decreaseYear : decreaseMonth}
              disabled={prevMonthButtonDisabled}
              className="px-2 py-1"
            >
              {"<"}
            </button>
            <button
              type="button"
              className="text-lg font-semibold"
              onClick={handleYearMonthClick}
            >
              {date.toLocaleString("ko-KR", {
                year: "numeric",
                month: "long",
              })}
            </button>
            <button
              onClick={showMonthPicker ? increaseYear : increaseMonth}
              disabled={nextMonthButtonDisabled}
              className="px-2 py-1"
            >
              {">"}
            </button>
          </div>
        )}
      />
    </div>
  );
};

export default DatepickerComponent;
