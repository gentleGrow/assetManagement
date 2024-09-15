// utils/indexedDB.js
export const openDB = () => {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open("stockDatabase", 1);

    request.onupgradeneeded = (event: any) => {
      const db = event.target?.result;
      if (!db.objectStoreNames.contains("stocks")) {
        db.createObjectStore("stocks", { keyPath: "code" }); // code를 키로 사용
      }
    };

    request.onsuccess = (event: any) => {
      resolve(event.target?.result);
    };

    request.onerror = (event: any) => {
      reject("Database error: " + event.target?.errorCode);
    };
  });
};