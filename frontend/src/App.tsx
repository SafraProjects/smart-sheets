// App.tsx
import React from "react";
import "./App.css";
import { LanguageProvider } from "../contexts/languageContext";
import { RoutingRoot } from "./routeRoots";

export const App: React.FC = (): any => {
  return (
    <LanguageProvider>
      <RoutingRoot />
    </LanguageProvider>
  );
};
