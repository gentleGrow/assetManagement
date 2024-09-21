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

export async function updateStockAsset(stockAsset) {
  try {
    const response = await fetch(`/api/v1/assetstock`, {
      method: "PUT",
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

export async function deleteStockAsset(assetId) {
  try {
    const response = await fetch(`/api/v1/assetstock/${assetId}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
    });
    if (!response.ok) throw new Error("Failed to create stock asset");
    return await response.json();
  } catch (error) {
    console.error("Error creating stock asset:", error);
  }
}
