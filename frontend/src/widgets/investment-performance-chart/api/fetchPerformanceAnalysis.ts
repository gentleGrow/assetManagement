import { LineChartData, SERVICE_SERVER_URL } from "@/shared";

const fetchPerformanceAnalysis = async (): Promise<LineChartData> => {
  try {
    const response = await fetch(
      `${SERVICE_SERVER_URL}/api/chart/v1/dummy/performance-analysis`,
    );
    if (!response.ok) {
      throw new Error(`${response.status}: ${await response.json()}`);
    }
    const performanceAnalysis = await response.json();
    return performanceAnalysis;
  } catch (error) {
    console.error(error);
    return {
      xAxises: [],
      values1: { values: [], name: "" },
      values2: { values: [], name: "" },
      unit: "",
    };
  }
};

export default fetchPerformanceAnalysis;
