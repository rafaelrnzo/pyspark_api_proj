// config.ts

interface Config {
    baseURL: string;
    websocketURL: string;
  }
  
  const LOCAL_CONFIG: Config = {
    baseURL: "http://127.0.0.1:8000",
    websocketURL: "ws://127.0.0.1:8000",
  };
  
  const DEV_CONFIG: Config = {
    baseURL: "http://127.0.0.1:8000",
    websocketURL: "ws://127.0.0.1:8000",
  };
  
  const PROD_CONFIG: Config = {
    baseURL: "https://api.example.com",
    websocketURL: "wss://api.example.com",
  };
  
  const getConfig = (): Config => {
    switch (process.env.NODE_ENV) {
      case "production":
        return PROD_CONFIG;
      case "development":
        return DEV_CONFIG;
      case "test":
        return LOCAL_CONFIG;
      default:
        return LOCAL_CONFIG; // Default to local for safety
    }
  };
  
  
  export const config = getConfig();
  