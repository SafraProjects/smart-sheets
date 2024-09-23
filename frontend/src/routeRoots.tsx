import React from "react";
import { HomePage } from "./pages/home/homePage";
import { UserPage } from "./pages/users/userPage";
import { Route, Routes, useLocation } from "react-router-dom";

export const RoutingRoot: React.FC = () => {
  // const location = useLocation();
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/a" element={<UserPage />} />
    </Routes>
  );
};