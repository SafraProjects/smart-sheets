import React, { createContext, useContext, useEffect, useState } from "react";
import {
  KeyLanguageWords,
  Language,
  LanguageContextProps,
  LanguageProviderProps,
} from "./contextsTyps";
import texts from "./engesh-WordsAndDirections.json";

export const LanguageContext = createContext<LanguageContextProps | undefined>(
  undefined
);

export const LanguageProvider: React.FC<LanguageProviderProps> = ({
  children,
}) => {
  const [language, setLanguage] = useState<Language>("he");

  useEffect(() => {
    const savedLanguage = localStorage.getItem("appLanguage") as Language;
    if (savedLanguage) {
      setLanguage(savedLanguage);
    }
  }, []);

  const toggleLanguage = () => {
    const newLanguage = language === "he" ? "en" : "he";
    setLanguage(newLanguage);
    localStorage.setItem("appLanguage", newLanguage);
  };

  const getText = (key: KeyLanguageWords) => texts[language][key] || key;

  return (
    <LanguageContext.Provider value={{ language, toggleLanguage, getText }}>
      <div dir={language === "he" ? "rtl" : "ltr"}>{children}</div>
    </LanguageContext.Provider>
  );
};

export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error("useLanguage must be used within a LanguageProvider");
  }
  return context;
};
