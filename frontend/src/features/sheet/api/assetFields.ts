export async function getAssetFields() {
  try {
    const response = await fetch(`/api/v1/asset-field`, {
      headers: {
      },
    });

    if (!response.ok) throw new Error("Failed to fetch asset fields");
    const data = await response.json();

    return data;
  } catch (error) {
    console.error("Error fetching asset fields:", error);
    return [];
  }
}

export async function modifyAssetFields(fieldList) {
  try {
    const response = await fetch(`/api/v1/asset-field`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(fieldList),
    });

    if (!response.ok) throw new Error("Failed to modify asset fields");
    const data = await response.json();

    return data;
  } catch (error) {
    console.error("Error modifying asset fields:", error);
    return [];
  }
}
