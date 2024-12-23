"use client";

import React, { useEffect, useState } from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import CountCard from "./components/countingCard";
import { fetchDataFromAPI, setupWebSocket } from "./utils/api_utils";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const CountDataChart: React.FC = () => {
  const [count, setCount] = useState<number[]>([]);
  const [labels, setLabels] = useState<string[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [totalCount, setTotalCount] = useState<number | null>(null);

  useEffect(() => {
    fetchDataFromAPI("/kafka/all-data", setCount, setLabels, setError);
  }, []);

  useEffect(() => {
    const ws = setupWebSocket("ws/count-data", setTotalCount);
    return () => {
      ws.close();
    };
  }, []);

  const chartData = {
    labels,
    datasets: [
      {
        label: "Order Count",
        data: count,
        backgroundColor: "rgba(37, 99, 235, 0.3)",
        borderColor: "rgba(37, 99, 235, 1)",
        pointBackgroundColor: "#ffffff",
        pointBorderColor: "rgba(37, 99, 235, 1)",
        pointHoverBackgroundColor: "rgba(37, 99, 235, 1)",
        pointHoverBorderColor: "#ffffff",
        fill: true,
        tension: 0.4,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        position: "top" as const,
        labels: {
          font: { size: 14, weight: "bold" },
        },
      },
      tooltip: {
        callbacks: {
          label: (tooltipItem: any) => `Order Count: ${tooltipItem.raw}`,
        },
      },
    },
    scales: {
      y: {
        title: { display: true, text: "Order Count", font: { size: 14, weight: "bold" } },
        ticks: { beginAtZero: true, stepSize: 1, font: { size: 12 } },
      },
      x: {
        title: { display: true, text: "Labels", font: { size: 14, weight: "bold" } },
        ticks: { font: { size: 12 } },
      },
    },
  };

  return (
    <div className="p-8">
      <div className="flex flex-col gap-y-6">
        <h1 className="text-3xl">Order Count Visualization</h1>
        <div className="flex gap-x-4">
          <CountCard totalCount={totalCount} title="Total Order Count" />
          <CountCard totalCount={totalCount} title="Total Order Count" />
        </div>
        <div className="bg-white/5 p-6 rounded-xl border-white/15 border">
          {error ? (
            <p style={{ color: "red", textAlign: "center" }}>{error}</p>
          ) : chartData.labels.length > 0 ? (
            <div className="w-auto h-80">
              <Line data={chartData} options={options} />
            </div>
          ) : (
            <p style={{ textAlign: "center" }}>Loading data...</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default CountDataChart;
