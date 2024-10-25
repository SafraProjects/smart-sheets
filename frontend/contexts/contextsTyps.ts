export type Language = "he" | "en";

export type KeyLanguageWords =
  | "button"
  | "tableTitle"
  | "uploadedFile"
  | "createTable"
  | "tableFieldPlaceholder"
  | "emailInputLabel"
  | "passwordInputLabel"
  | "resend"
  | "singUp"
  | "login"
  | "loading"
  | "cancel"
  | "confirm"
  | "yes"
  | "no"
  | "secondPasswordInputLabel"
  | "userNameInputLabel"
  | "recreatePassword"
  | "createAccount"
  | "passwordsDoNotMatch"
  | "alertEmailMessage"
  | "verifyEmailMessage"
  | "SandPasswordToEmailMessage"
  | "expireVerificationTokenMessage"
  | "EmailSandMessage";

export interface LanguageTextInterface {
  he: {
    [key in KeyLanguageWords]: string;
  };
  en: {
    [key in KeyLanguageWords]: string;
  };
}

export interface LanguageContextProps {
  language: Language;
  toggleLanguage: () => void;
  getText: (key: KeyLanguageWords) => string;
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
