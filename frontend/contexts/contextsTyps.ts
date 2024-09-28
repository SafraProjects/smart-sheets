import React from "react";

export type Language = "he" | "en";
export type KeyLanguageWords = "button";

export interface LanguageContextProps {
  language: Language;
  toggleLanguage: () => void;
  getText: (key: KeyLanguageWords) => string;
}

export interface LanguageProviderProps {
  children: React.ReactNode;
}

export interface LanguageContextProps {
  language: Language;
  toggleLanguage: () => void;
  getText: (key: KeyLanguageWords) => string;
}

// contextTypes.ts
export interface User {
  id: string;
  name: string;
  email: string;
}

export interface languageTextInterface {
  he: { [key in KeyLanguageWords]: string };
  en: { [key in KeyLanguageWords]: string };
}
