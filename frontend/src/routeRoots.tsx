import React from "react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";

import { HomePage } from "./pages/home/homePage";
import { UserPage } from "./pages/users/userPage";
import { Auto } from "./pages/Access/Auto";
import { Login } from "./pages/Access/login/Login";
import { SingUp } from "./pages/Access/singUp/SingUp";
// import { Navigate, Route, Routes } from "react-router-dom";
// import TableFieldInput from "./components/FieldInput";
// import FileUpload from "./components/uploadFile";

const router = createBrowserRouter([
  {
    path: "/",
    element: <HomePage />,
    errorElement: <div>404 Not Found</div>,
  },
  {
    path: "/user",
    element: <UserPage />,
  },
  {
    path: "/auto",
    element: <Auto url={null} />,
    children: [
      {
        path: "/auto/sing-up",
        element: <SingUp />,
      },
      {
        path: "/auto/log-in",
        element: <Login />,
      },
      // need some adjustment for handel recreate user password with email verification
      {
        path: "/auto/recreate-password",
        // element: <Login />,
      },
    ],
  },
  {
    path: "/auto/verify-email",
    element: <Auto url={"verify-email"} />,
  },
]);

export const RoutingRoot: React.FC = () => {
  return <RouterProvider router={router} />;
};
