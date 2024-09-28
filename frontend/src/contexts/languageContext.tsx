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
  const [language, setLanguage] = useState<Language>("he"); // ברירת מחדל לעברית
  const [isLoading, setIsLoading] = useState(true); // מצב טעינה

  useEffect(() => {
    const savedLanguage = localStorage.getItem("appLanguage") as Language;
    if (savedLanguage) {
      setLanguage(savedLanguage);
    }
    setIsLoading(false);
  }, []);

  useEffect(() => {
    if (language) {
      document.documentElement.setAttribute(
        "dir",
        language === "he" ? "rtl" : "ltr"
      );
    }
  }, [language]);

  const toggleLanguage = () => {
    const newLanguage = language === "he" ? "en" : "he";
    setLanguage(newLanguage);
    localStorage.setItem("appLanguage", newLanguage);
  };

  const getText = (key: KeyLanguageWords) => {
    if (!language || isLoading) {
      return key; // אם השפה עדיין לא נטענה, החזר את המפתח
    }
    return texts[language][key] || key;
  };

  // הוספת key לקומפוננטה להבטחת רינדור מחדש
  return (
    <LanguageContext.Provider value={{ language, toggleLanguage, getText }}>
      <div key={language}>{children}</div>
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
