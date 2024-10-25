import React, { useEffect, useState } from "react";
import { Link, Outlet, useLocation } from "react-router-dom";
import "./auto.css";
// import logo from "/assets/tabio2.png";
import { useLanguage } from "../../../contexts/languageContext";
import logo2 from "/assets/tabio.png";

export const Auto: React.FC = () => {
  const [path, setPath] = useState<"sing-up" | "log-in" | "">();

  const { getText } = useLanguage();

  const location = useLocation();

  useEffect(() => {
    if (location.pathname === "/auto/sing-up") {
      setPath("sing-up");
    } else if (location.pathname === "/auto/log-in") {
      setPath("log-in");
    }
  }, [location]);

  return (
    <div className="log-back">
      <div className="from-user-login">
        <div className="from-header">
          <Link to="sing-up" className="custom-link">
            <div
              className={`first url-button ${
                path === "sing-up" ? "active" : "un-active"
              }`}
            >
              <h3>{getText("singUp")}</h3>
            </div>
          </Link>
          <Link to="log-in" className="custom-link">
            <div
              className={`url-button ${
                path === "log-in" ? "active" : "un-active"
              }`}
            >
              <h3>{getText("login")}</h3>
            </div>
          </Link>
        </div>
        <img src={logo2} alt="tabio logo" width="140px" height="50px" />
        <div className="from">
          <div className="input-area">
            <Outlet />
          </div>
        </div>
      </div>
    </div>
  );
};
