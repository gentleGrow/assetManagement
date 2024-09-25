"use client";
import { useEffect } from "react";
import * as echarts from "echarts";
import { BarChartData } from "../types/charts";

export default function BarChart({ chartData }: { chartData: BarChartData }) {
  useEffect(() => {
    const chartDom = document.getElementById("chart");
    const myChart = echarts.init(chartDom);

    const option = {
      grid: {
        left: "17px",
        right: "6px",
        bottom: "0%",
        containLabel: true,
      },
      tooltip: {
        trigger: "item",
        formatter: function (params) {
          return `${(params.value * 10000).toLocaleString("ko-kr")}원`;
        },
        position: function (point, params, dom, rect, size) {
          if (rect) {
            const tooltipWidth = size.contentSize[0];
            const tooltipHeight = size.contentSize[1];

            let posX = rect.x + rect.width / 2 - tooltipWidth / 2;
            let posY = rect.y - tooltipHeight - 10;

            const viewWidth = size.viewSize[0];
            const viewHeight = size.viewSize[1];

            if (posX < 0) {
              posX = 0;
            } else if (posX + tooltipWidth > viewWidth) {
              posX = viewWidth - tooltipWidth;
            }

            if (posY < 0) {
              posY = rect.y + rect.height + 10;
            }

            return [posX, posY];
          } else {
            return [point[0], point[1] - size.contentSize[1] - 10];
          }
        },
        axisPointer: {
          type: "shadow",
        },
        backgroundColor: "#fff",
        borderColor: "#fff",
        borderWidth: 1,
        textStyle: {
          color: "#2A2D31",
          fontWeight: 600,
          fontSize: 12,
        },
        appendToBody: true,
        extraCssText: `
            box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
            &::after { display: none; }
        `,
      },
      xAxis: {
        type: "category",
        data: chartData.xAxises,
        axisLabel: {
          interval: 0,
          margin: 12,
        },
        splitLine: {
          show: false,
        },
        axisTick: {
          show: false,
        },
        textStyle: {
          color: "#4F555E",
          fontSize: 12,
          fontWeight: 400,
          lineHeight: 14.4,
        },
      },
      yAxis: {
        type: "value",
        name: `(${chartData.unit})`,
        min: 0,
        max: 50,
        axisLabel: {
          margin: 12,
        },
        nameLocation: "end",
        nameTextStyle: {
          align: "right",
          padding: 3,
        },
        nameGap: 12,
        textStyle: {
          color: "#4F555E",
          fontSize: 12,
          fontWeight: 400,
          lineHeight: 14.4,
        },
      },
      series: [
        {
          type: "bar",
          data: chartData.data,
          itemStyle: {
            color: "rgba(5, 214, 101, 0.5)",
            borderColor: "#05D665",
            barBorderRadius: [5, 5, 0, 0],
          },
          emphasis: {
            focus: "none",
            itemStyle: {
              color: "#05D665",
            },
          },
          barWidth: "40%",
        },
      ],
    };

    myChart.setOption(option);

    window.addEventListener("resize", () => {
      myChart.resize();
    });

    return () => {
      window.removeEventListener("resize", () => {
        myChart.resize();
      });
    };
  }, [chartData]);

  return <div id="chart" className="h-full w-full" />;
}
