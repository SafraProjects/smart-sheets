import React, { useState } from "react";
import { Link, Outlet, useParams } from "react-router-dom";
import "./auto.css";
// import logo from "/assets/tabio2.png";
import logo2 from "/assets/tabio.png";
import { Login } from "./login/Login";
import { useLanguage } from "../../../contexts/languageContext";
import { VerifyEmail } from "./verification/verifyEmail";

export const Auto: React.FC<{ url: "verify-email" | null }> = ({
  url = null,
}) => {
  const [path, usePath] = useState<"sing-up" | "log-in" | "">();
  const { getText } = useLanguage();

  const hendelClickPath = (path: "sing-up" | "log-in") => {
    usePath(path);
  };

  const handelSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // כאן תכניס את הלוגיקה שלך עבור שליחת הטופס
  };

  return (
    <>
      <div className="log-back">
        {url === null ? (
          <form className="from-user-login" onSubmit={handelSubmit}>
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
                <div
                  className={`url-button ${path === "log-in" ? "active" : ""}`}
                >
                  <h3>{getText("login")}</h3>
                </div>
              </Link>
            </div>
            <img src={logo2} alt="tabio logo" width="170px" height="50px" />

            <Outlet />
          </form>
        ) : (
          <VerifyEmail />
        )}
      </div>
    </>
  );
};
