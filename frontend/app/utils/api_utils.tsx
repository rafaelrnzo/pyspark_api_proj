// utils.ts
import { config } from "./config";

export interface ApiResponse {
  status: string;
  data: { order_count: number }[];
}

export const fetchDataFromAPI = async (
  endpoint: string,
  setCount: React.Dispatch<React.SetStateAction<number[]>>,
  setLabels: React.Dispatch<React.SetStateAction<string[]>>,
  setError: React.Dispatch<React.SetStateAction<string | null>>
): Promise<void> => {
  try {
    const url = `${config.baseURL}${endpoint}`;
    const response = await fetch(url);
    const result: ApiResponse = await response.json();
    console.log("API Response:", result);

    if (result.status === "success" && Array.isArray(result.data)) {
      setCount(result.data.map((item) => item.order_count || 0));
      setLabels(result.data.map((_, index) => `Label ${index + 1}`));
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

export const setupWebSocket = (
  endpoint: string,
  setTotalCount: React.Dispatch<React.SetStateAction<number | null>>
): WebSocket => {
  // Ensure there is a single "/" between websocketURL and endpoint
  const url = `${config.websocketURL.replace(/\/$/, "")}/${endpoint.replace(/^\//, "")}`;
  
  const ws = new WebSocket(url);

  ws.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data) as { status: string; total_order_count: number };
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

  return ws;
};

