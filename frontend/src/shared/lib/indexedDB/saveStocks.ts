import { openDB } from "./openDB";

export const saveStocks = async (stocks) => {
  const db: any = await openDB();
  const transaction = db?.transaction("stocks", "readwrite");
  const store = transaction.objectStore("stocks");

  stocks.forEach((stock) => {
    store.put(stock);
  });

  return transaction.complete;
};