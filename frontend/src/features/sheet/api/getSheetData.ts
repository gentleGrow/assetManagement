import { SERVICE_SERVER_URL } from "@/shared/constants/api";
const API_URL = `${SERVICE_SERVER_URL}/api/v1`;

export async function getStockAssets(isKRW = true) {
  try {
    const params = new URLSearchParams({ base_currency: isKRW.toString() });
    const response = await fetch(`/api/v1/assetstock?${params}`, {});

    if (!response.ok) throw new Error("Failed to fetch stock assets");
    const data = await response.json();

    const { stock_assets } = data;

    return data;
  } catch (error) {
    console.error("Error fetching stock assets:", error);
    return [];
  }
}
