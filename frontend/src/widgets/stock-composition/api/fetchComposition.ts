import { DonutChartData, SERVICE_SERVER_URL } from "@/shared";

const fetchComposition = async (
  type: "composition" | "account" = "composition",
): Promise<DonutChartData[]> => {
  try {
    const response = await fetch(
      `${SERVICE_SERVER_URL}/api/chart/v1/dummy/composition?type=${type}`,
    );
    if (!response.ok) {
      throw new Error(`${response.status}: ${await response.json()}`);
    }
    const composition = await response.json().then((data) => data.composition);
    return composition;
  } catch (error) {
    console.error(error);
    return [];
  }
};

export default fetchComposition;
