import React from "react";
import { useLanguage } from "../contexts/languageContext";

const SideOptions: React.FC = () => {
  const { language, toggleLanguage, getText } = useLanguage();

  return (
    <div className="side-options">
      <button onClick={toggleLanguage}>{getText("button")}</button>
    </div>
  );
};

export default SideOptions;
