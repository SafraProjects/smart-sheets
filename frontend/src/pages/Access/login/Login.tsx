import React, { useState } from "react";
import { useLanguage } from "../../../../contexts/languageContext";

export const Login: React.FC = () => {
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const { getText } = useLanguage();

  return (
    <div className="input-area">
      <h4>{getText("login")}</h4>
      <div className="input-container">
        <input
          type="email"
          id="emailInput"
          placeholder=" "
          aria-label="Email"
          maxLength={50}
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <label htmlFor="emailInput">{getText("emailInputLabel")}</label>
      </div>

      <div className="input-container">
        <input
          type="password"
          id="passwordInput"
          placeholder=" "
          minLength={6}
          maxLength={12}
          aria-label="Password"
          required
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <label htmlFor="passwordInput">{getText("passwordInputLabel")}</label>
      </div>

      <button
        className={!email || !password ? "" : "submit"}
        type="submit"
        disabled={!email || !password}
      >
        {getText("submit")}
      </button>
    </div>
  );
};
