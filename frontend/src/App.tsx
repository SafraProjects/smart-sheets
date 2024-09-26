// App.tsx
import React from "react";
import { BrowserRouter as Router } from "react-router-dom";
import "./App.css";
import { LanguageProvider } from "./contexts/languageContext";
import { RoutingRoot } from "./routeRoots";

export const App: React.FC = (): any => {
  return (
    <LanguageProvider>
      <Router>
        <RoutingRoot />
      </Router>
    </LanguageProvider>
  );
};
