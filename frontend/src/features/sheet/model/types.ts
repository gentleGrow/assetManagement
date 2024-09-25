export type Asset = {
  id: 0;
  account_type: string;
  buy_date: string;
  current_price: number;
  dividend: number;
  highest_price: number;
  investment_bank: string;
  lowest_price: number;
  opening_price: number;
  profit_rate: number;
  profit_amount: number;
  purchase_amount: number;
  purchase_price: number;
  purchase_currency_type: string;
  quantity: number;
  stock_code: string;
  stock_name: string;
  stock_volume: number;
};

export const stockAssets: Asset[] = [
  {
    id: 0,
    account_type: "ISA",
    buy_date: "2024-09-06",
    current_price: 0,
    dividend: 0,
    highest_price: 0,
    investment_bank: "토스증권",
    lowest_price: 0,
    opening_price: 0,
    profit_rate: 0,
    profit_amount: 0,
    purchase_amount: 0,
    purchase_price: 0,
    purchase_currency_type: "KRW",
    quantity: 0,
    stock_code: "AAPL",
    stock_name: "BGF리테일",
    stock_volume: 0,
  },
];
