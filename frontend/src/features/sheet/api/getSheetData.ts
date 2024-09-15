import { SERVICE_SERVER_URL } from "@/shared/constants/api";
const API_URL = `${SERVICE_SERVER_URL}/api/v1`;

export async function getStockAssets() {
  try {
    // const response = await fetch(`${API_URL}/assetstock`);
    const response = await fetch(`/api/v1/assetstock`);

    if (!response.ok) throw new Error("Failed to fetch stock assets");
    const data = await response.json();

    const { stock_assets } = data;

    return stock_assets;
  } catch (error) {
    console.error("Error fetching stock assets:", error);
  }
}

export async function getDummyStockAssets() {
  try {
    const response = await fetch(`/api/v1/dummy/assetstock`);
    if (!response.ok) throw new Error("Failed to fetch stock assets");

    const data = await response.json();

    const { stock_assets } = data;

    return stock_assets;
  } catch (error) {
    console.error("Error fetching stock assets:", error);
  }
}

export async function createStockAsset(stockAsset) {
  try {
    const response = await fetch(`/api/v1/assetstock`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(stockAsset),
    });
    if (!response.ok) throw new Error("Failed to create stock asset");
    return await response.json();
  } catch (error) {
    console.error("Error creating stock asset:", error);
  }
}
