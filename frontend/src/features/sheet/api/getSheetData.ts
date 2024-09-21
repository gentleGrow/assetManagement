import { SERVICE_SERVER_URL } from "@/shared/constants/api";
const API_URL = `${SERVICE_SERVER_URL}/api/v1`;

export async function getStockAssets() {
  try {
    const response = await fetch(`/api/v1/assetstock`, {});

    if (!response.ok) throw new Error("Failed to fetch stock assets");
    const data = await response.json();

    const { stock_assets } = data;

    return data;
  } catch (error) {
    console.error("Error fetching stock assets:", error);
    return [];
  }
}
