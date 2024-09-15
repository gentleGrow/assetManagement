export async function getAllStocks() {
  try {
    const response = await fetch(`/api/v1/stocks`);
    if (!response.ok) throw new Error("Failed to fetch stock list");

    const data = await response.json();

    const { stock_list } = data;

    return Array.isArray(stock_list) ? [...stock_list] : [];
  } catch (error) {
    console.error("Error fetching stock list:", error);
    return [];
  }
}

export async function getAllOptions() {
  try {
    const response = await fetch(`/api/v1/bank-accounts`);
    if (!response.ok) throw new Error("Failed to fetch bank/account list");

    const data = await response.json();

    const { investment_bank_list, account_list } = data;

    return {
      bankList: Array.isArray(investment_bank_list)
        ? investment_bank_list.map((bank) => ({ id: bank, name: bank }))
        : [],
      accountList: Array.isArray(account_list)
        ? account_list.map((accountType) => ({
            id: accountType,
            name: accountType,
          }))
        : [],
    };
  } catch (error) {
    console.error("Error fetching bank/account list", error);
    return {bankList: [], accountList: []};
  }
}
