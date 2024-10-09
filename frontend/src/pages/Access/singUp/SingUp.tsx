import React, { useState } from "react";
import { useLanguage } from "../../../../contexts/languageContext";

export const SingUp: React.FC = () => {
  const [name, setName] = useState<string>("");
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [secondPassword, setSecondPassword] = useState<string>("");
  const { getText } = useLanguage();

  return (
    <div className="input-area">
      <h4>{getText("singUp")}</h4>
      <div className="input-container">
        <input
          type="text"
          id="nameInput"
          placeholder=" "
          aria-label="name"
          maxLength={50}
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
        <label htmlFor="nameInput">{getText("userNameInputLabel")}</label>
      </div>

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

      <div className="input-container">
        <input
          type="password"
          id="secondPasswordInput"
          placeholder=" "
          minLength={6}
          maxLength={12}
          aria-label="secondPassword"
          required
          value={secondPassword}
          onChange={(e) => setSecondPassword(e.target.value)}
        />
        <label htmlFor="secondPasswordInput">
          {getText("secondPasswordInputLabel")}
        </label>
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
