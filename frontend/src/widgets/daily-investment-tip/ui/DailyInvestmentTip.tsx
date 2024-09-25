import fetchTodayTip from "../api/fetchTodayTip";

export default async function DailyInvestmentTip() {
  const todayTip = await fetchTodayTip();
  return (
    <div className="flex items-center space-x-[20px] rounded-md border border-gray-20 p-[16px] mobile:flex-col mobile:items-start mobile:space-x-0 mobile:space-y-[20px] mobile:rounded-none mobile:border-none mobile:px-[20px]">
      <h3 className="block shrink-0 text-heading-2">오늘의 투자 tip</h3>
      <div className="flex w-full grow items-center space-x-[8px] border border-green-20 bg-green-10/30 px-[16px] py-[13px]">
        <svg
          width="18"
          height="18"
          viewBox="0 0 18 18"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <rect x="1" y="1" width="16" height="16" fill="#C3F5DA" />
          <path
            d="M14 14H12V9H14V14ZM6 14H4V4H6V14ZM10 14H8V7H10V14ZM16 18C16.55 18 17.0208 17.8042 17.4125 17.4125C17.8042 17.0208 18 16.55 18 16V2C18 1.45 17.8042 0.979167 17.4125 0.5875C17.0208 0.195833 16.55 0 16 0H2C1.45 0 0.979166 0.195833 0.5875 0.5875C0.195833 0.979167 0 1.45 0 2V16C0 16.55 0.195833 17.0208 0.5875 17.4125C0.979166 17.8042 1.45 18 2 18H16ZM16 16H2V2H16V16Z"
            fill="#05D665"
          />
        </svg>

        <p className="block text-[14px] font-semibold leading-[22px] text-gray-100">
          {todayTip}
        </p>
      </div>
    </div>
  );
}
