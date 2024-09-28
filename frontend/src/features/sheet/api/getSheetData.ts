import { SERVICE_SERVER_URL } from "@/shared/constants/api";
const API_URL = `${SERVICE_SERVER_URL}/api/v1`;

export async function getStockAssets(isKRW = true) {
  try {
    const response = await fetch(`/api/v1/sample/assetstock`, {});

    if (!response.ok) throw new Error("Failed to fetch stock assets");
    const data = await response.json();

    return data;
  } catch (error) {
    console.error("Error fetching stock assets:", error);
    return [];
  }
}
