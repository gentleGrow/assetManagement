import { SERVICE_SERVER_URL } from "@/shared";

const fetchTodayTip = async (): Promise<string> => {
  try {
    const response = await fetch(`${SERVICE_SERVER_URL}/api/chart/v1/tip`);
    if (!response.ok) {
      throw new Error(`${response.status}: ${await response.json()}`);
    }
    const todayTip = await response.json().then((data) => data.today_tip);
    return todayTip;
  } catch (error) {
    console.error(error);
    return "오늘의 투자 팁을 가져오지 못했어요.";
  }
};

export default fetchTodayTip;
