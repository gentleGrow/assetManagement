import { SERVICE_SERVER_URL } from "@/shared";
interface Indices {
  index_name: string;
  index_name_kr: string;
  current_value: number;
  change_percent: number;
}
const fetchIndices = async (): Promise<Indices[]> => {
  try {
    const response = await fetch(`${SERVICE_SERVER_URL}/api/chart/v1/indice`);
    if (!response.ok) {
      throw new Error(`${response.status}: ${await response.json()}`);
    }
    const indices = await response.json().then((data) => data.market_indices);
    return indices;
  } catch (error) {
    console.error(error);
    return [];
  }
};
export default fetchIndices;
