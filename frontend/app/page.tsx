"use client"; // Ensure this is at the very top

import React, { useEffect, useState } from "react";
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
import { Line } from "react-chartjs-2";
import CountCard from "./components/countingCard";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const CountDataChart: React.FC = () => {
  const [count, setCount] = useState<number[]>([]);
  const [labels, setLabels] = useState<string[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [totalCount, setTotalCount] = useState<number | null>(null);

  // Fetch data from API
  const fetchData = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/all-data");
      const result = await response.json();
      console.log("API Response:", result);

      if (result.status === "Spark job completed" && Array.isArray(result.data)) {
        setCount(result.data.map((item: any) => item.order_count || 0)); // Assuming `order_count` is a field
        setLabels(result.data.map((item: any, index: number) => `Label ${index + 1}`)); // Generate labels dynamically
        setError(null);
      } else {
        console.error("Unexpected data format from the API:", result);
        setError("Unexpected data format from the API.");
      }
    } catch (error) {
      console.error("Error fetching data:", error);
      setError("Failed to fetch data from the API.");
    }
  };

  // WebSocket connection to get the total count
  useEffect(() => {
    const ws = new WebSocket("ws://127.0.0.1:8000/ws/count-data");

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.status === "success" && typeof data.total_order_count === "number") {
          setTotalCount(data.total_order_count);
        } else {
          console.error("Unexpected WebSocket data format:", data);
        }
      } catch (error) {
        console.error("Error parsing WebSocket message:", error);
      }
    };

    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    ws.onclose = () => {
      console.log("WebSocket connection closed.");
    };

    return () => {
      ws.close();
    };
  }, []);

  useEffect(() => {
    fetchData();
  }, []);

  // Line Chart Data
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
        tension: 0.4, // Smoother curve for the line
      },
    ],
  };

  // Line Chart Options
  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        position: "top" as const,
        labels: {
          font: {
            size: 14,
            weight: "bold",
          },
        },
      },
      tooltip: {
        enabled: true,
        mode: "index",
        intersect: false,
        callbacks: {
          label: (tooltipItem: any) => `Order Count: ${tooltipItem.raw}`,
        },
      },
    },
    scales: {
      y: {
        title: {
          display: true,
          text: "Order Count",
          font: {
            size: 14,
            weight: "bold",
          },
        },
        ticks: {
          beginAtZero: true,
          stepSize: 1,
          font: {
            size: 12,
          },
        },
      },
      x: {
        title: {
          display: true,
          text: "Labels",
          font: {
            size: 14,
            weight: "bold",
          },
        },
        ticks: {
          font: {
            size: 12,
          },
        },
      },
    },
  };

  return (
    <div className="p-8">
      <div className="flex flex-col gap-y-6">
          <h1 className="text-3xl">Order Count Visualization</h1>
          <div className="flex gap-x-4">
            <CountCard totalCount={totalCount} title="Total Order Count"/>
            <CountCard totalCount={totalCount} title="Total Order Count"/>
            <CountCard totalCount={totalCount} title="Total Order Count"/>
            <CountCard totalCount={totalCount} title="Total Order Count"/>
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
