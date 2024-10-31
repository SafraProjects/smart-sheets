import { createContext } from "react";

// טיפוסים
export type WebSocketData = {
  [key: string]: any;
};

export interface GlobalWebSocketContextProps {
  data: WebSocketData;
  connectWebSocket: () => void;
}

// יצירת הקונטקסט עם ערך התחלתי ריק
export const GlobalWebSocketContext = createContext<GlobalWebSocketContextProps | undefined>(undefined);
