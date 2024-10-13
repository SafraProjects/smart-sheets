import React, { useState } from "react";
import { Link, Outlet } from "react-router-dom";
import "./auto.css";
// import logo from "/assets/tabio2.png";
import { useLanguage } from "../../../contexts/languageContext";
import logo2 from "/assets/tabio.png";

export const Auto: React.FC = () => {
  const [path, usePath] = useState<"sing-up" | "log-in" | "">();

  const { getText } = useLanguage();

  const hendelClickPath = (path: "sing-up" | "log-in") => {
    usePath(path);
  };

  return (
    <div className="log-back">
      <div className="from-user-login">
        <div className="from-header">
          <Link
            to="sing-up"
            onClick={() => hendelClickPath("sing-up")}
            className="custom-link"
          >
            <div
              className={`first url-button ${
                path === "sing-up" ? "active" : ""
              }`}
            >
              <h3>{getText("singUp")}</h3>
            </div>
          </Link>
          <Link
            to="log-in"
            onClick={() => hendelClickPath("log-in")}
            className="custom-link"
          >
            <div className={`url-button ${path === "log-in" ? "active" : ""}`}>
              <h3>{getText("login")}</h3>
            </div>
          </Link>
        </div>
        <img src={logo2} alt="tabio logo" width="130px" height="40px" />
        <div className="from">
          <div className="input-area">
            <Outlet />
          </div>
        </div>
      </div>
    </div>
  );
};
