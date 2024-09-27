import React from "react";
import { Route, Routes } from "react-router-dom";
import TableFieldInput from "./components/FieldInput";
import { HomePage } from "./pages/home/homePage";
import { UserPage } from "./pages/users/userPage";

export const RoutingRoot: React.FC = () => {
  return (
    <Routes>
      <Route path="/" element={<HomePage />}>
        <Route path="b" element={<TableFieldInput />} />
      </Route>

      <Route path="/user/*" element={<UserPage />}>
        <Route path="a" element={<UserPage />} />
      </Route>
    </Routes>
  );
};
