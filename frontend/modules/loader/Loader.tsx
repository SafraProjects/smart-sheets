import React from "react";
import "./loader.css";
import { useLanguage } from "../../contexts/languageContext";

interface loaderProp {
  isOpen?: boolean;
  text?: string;
  shape?: "spin" | "move" | "dance" | "pop";
  // color?: string;
}

export const Loader: React.FC<loaderProp> = ({
  isOpen = true,
  shape = "spin",
  text,
  // color = "grey",
}) => {
  if (!isOpen) return null;
  const { getText } = useLanguage();
  return (
    <div className="loader-box">
      <h3>{text ? text : getText("loading")}</h3>
      <br />
      {shape !== "spin" ? (
        <div className="dots">
          <div className={`dot ${shape} one`}></div>
          <div className={`dot ${shape} two`}></div>
          <div className={`dot ${shape} three`}></div>
        </div>
      ) : (
        <div className="loader-area">
          <div className="loader"></div>
        </div>
      )}
    </div>
  );
};
