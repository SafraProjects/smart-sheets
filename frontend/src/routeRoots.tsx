import React from "react";
import { Route, Routes } from "react-router-dom";
import TableFieldInput from "./components/FieldInput";
import FileUpload from "./components/uploadFile";
import { HomePage } from "./pages/home/homePage";
import { UserPage } from "./pages/users/userPage";

export const RoutingRoot: React.FC = () => {
  return (
    <Routes>
      <Route path="/*" element={<HomePage />}>
        <Route path="b" element={<TableFieldInput />} />
      </Route>

      <Route path="u" element={<FileUpload />} />
      <Route path="/user" element={<UserPage />} />
    </Routes>
  );
};
