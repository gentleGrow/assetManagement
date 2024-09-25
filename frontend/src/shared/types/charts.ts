export interface LineChartValuesData {
  values: number[];
  name: string;
}

export interface LineChartData {
  xAxises: string[];
  values1: LineChartValuesData;
  values2: LineChartValuesData;
  unit: string;
}

export interface DonutChartData {
  name: string;
  percent_rate: number;
  current_amount: number;
}

export interface BarChartData {
  xAxises: string[];
  data: number[];
  unit: string;
}
