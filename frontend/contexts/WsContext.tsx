import React, {
  createContext,
  useState,
  useEffect,
  useContext,
  ReactNode,
} from "react";

// טיפוסים
type WebSocketData = {
  [key: string]: any;
};

interface GlobalWebSocketContextProps {
  data: WebSocketData;
  connectWebSocket: () => void;
}

// יצירת הקונטקסט עם ערך התחלתי ריק
const GlobalWebSocketContext = createContext<
  GlobalWebSocketContextProps | undefined
>(undefined);

interface GlobalWebSocketProviderProps {
  children: ReactNode;
}

// ספק הקונטקסט
export const GlobalWebSocketProvider: React.FC<
  GlobalWebSocketProviderProps
> = ({ children }) => {
  const [data, setData] = useState<WebSocketData>({});
  const [isConnected, setIsConnected] = useState<boolean>(false);

  useEffect(() => {
    let ws: WebSocket;

    if (isConnected) {
      ws = new WebSocket("ws://localhost:8000/ws");
      ws.onmessage = (event: MessageEvent) => {
        const message = JSON.parse(event.data);
        const { target, payload } = message;

        // עדכון אובייקט הנתונים לפי `target`
        setData((prevData) => ({
          ...prevData,
          [target]: payload,
        }));
      };

      // סגירת החיבור בעת יציאת המשתמש מהאתר
      const handleUnload = () => {
        ws.close();
      };
      window.addEventListener("beforeunload", handleUnload);

      // ניקוי האירועים וסגירת החיבור כאשר הקומפוננטה יוצאת מה-DOM
      return () => {
        ws.close();
        window.removeEventListener("beforeunload", handleUnload);
      };
    }
  }, [isConnected]);

  // פונקציה להפעלת החיבור
  const connectWebSocket = () => setIsConnected(true);

  return (
    <GlobalWebSocketContext.Provider value={{ data, connectWebSocket }}>
      {children}
    </GlobalWebSocketContext.Provider>
  );
};

// שימוש בקונטקסט בקומפוננטות
export const useWebSocketData = (target: string): any => {
  const context = useContext(GlobalWebSocketContext);
  if (!context) {
    throw new Error(
      "useWebSocketData must be used within a GlobalWebSocketProvider"
    );
  }
  return context.data[target];
};

// פונקציה לפתיחת החיבור מהקומפוננטות
export const useConnectWebSocket = (): (() => void) => {
  const context = useContext(GlobalWebSocketContext);
  if (!context) {
    throw new Error(
      "useConnectWebSocket must be used within a GlobalWebSocketProvider"
    );
  }
  return context.connectWebSocket;
};
