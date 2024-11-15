export type Language = "he" | "en";
export type KeyLanguageWords = "button" | "tableTitle" | "uploadedFile" | "createTable" | "tableFieldPlaceholder";

export interface LanguageContextProps {
  language: Language;
  toggleLanguage: () => void;
  getText: (key: KeyLanguageWords) => string;
}

export interface languageTextInterface {
  he: { [key in KeyLanguageWords]: string };
  en: { [key in KeyLanguageWords]: string };
}

export interface LanguageProviderProps {
  children: React.ReactNode;
}

// contextTypes.ts
export interface User {
  id: string;
  name: string;
  email: string;
}
