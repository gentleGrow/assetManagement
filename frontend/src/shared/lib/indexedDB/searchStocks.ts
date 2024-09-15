import { openDB } from "./openDB";

export const searchStocks = async (query) => {
  const db: any = await openDB();
  const transaction = db?.transaction("stocks", "readonly");
  const store = transaction.objectStore("stocks");

  return new Promise((resolve) => {
    const results: any[] = [];
    store.openCursor().onsuccess = (event) => {
      const cursor: any = event.target.result;
      if (cursor) {
        const { name, code } = cursor.value;
        if (name.toLowerCase().includes(query.toLowerCase())) {
          results.push(cursor.value);
        }
        cursor.continue();
      } else {
        resolve(results);
      }
    };
  });
};