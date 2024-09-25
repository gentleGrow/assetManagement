import { SERVICE_SERVER_URL } from "@/shared";

const fetchEstimateDividend = async (): Promise<any[]> => {
  try {
    const response = await fetch(
      `${SERVICE_SERVER_URL}/api/chart/v1/dummy/estimate-dividend`,
    );
    if (!response.ok) {
      throw new Error(`${response.status}: ${await response.json()}`);
    }
    const estimateDividend = await response
      .json()
      .then((data) => data.estimate_dividend_list);
    return estimateDividend;
  } catch (error) {
    console.error(error);
    return [];
  }
};

export default fetchEstimateDividend;
