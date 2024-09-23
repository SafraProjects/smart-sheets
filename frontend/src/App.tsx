import React from "react";
import { RoutingRoot } from "./routeRoots";
import "./App.css";
import { BrowserRouter as Router } from "react-router-dom";

export const App: React.FC = (): any => {
  return (
    <Router>
      <RoutingRoot />
    </Router>
  );
};
