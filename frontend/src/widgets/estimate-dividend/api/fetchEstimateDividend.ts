import { BarChartData, DonutChartData, SERVICE_SERVER_URL } from "@/shared";
import { ACCESS_TOKEN } from "@/shared/constants/cookie";
import { cookies } from "next/headers";

const fetchEstimateDividend = async (
  category: "every" | "type" = "every",
): Promise<BarChartData | DonutChartData[]> => {
  try {
    const response = await fetch(
      `${SERVICE_SERVER_URL}/api/chart/v1/estimate-dividend?category=${category}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + cookies().get(ACCESS_TOKEN),
        },
      },
    );
    if (!response.ok) {
      throw new Error(`${response.status}: ${await response.json()}`);
    }
    const estimateDividend = await response.json();

    return estimateDividend;
  } catch (error) {
    console.error(error);
    return [];
  }
};

export default fetchEstimateDividend;
