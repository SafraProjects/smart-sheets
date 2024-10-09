import React, { useState } from "react";
import { useLanguage } from "../../../../contexts/languageContext";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faEye, faEyeSlash } from "@fortawesome/free-solid-svg-icons";

export const SingUp: React.FC = () => {
  const [name, setName] = useState<string>("");
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [secondPassword, setSecondPassword] = useState<string>("");
  const [isPasswordVisible, setIsPasswordVisible] = useState(false);
  const [isSecondPasswordVisible, setIsSecondPasswordVisible] = useState(false);
  const { getText } = useLanguage();

  const togglePasswordVisibility = (num: number) => {
    if (num === 1) {
      setIsPasswordVisible(!isPasswordVisible);
    } else {
      setIsSecondPasswordVisible(!isSecondPasswordVisible);
    }
  };

  let validateSubmoit: boolean =
    !password ||
    !secondPassword ||
    password !== secondPassword ||
    (!email.includes("@") && !!email.includes(".")) ||
    !name;

  const handleSubmit = () => {
    // if
    // validate
  };

  return (
    <div className="input-area">
      <h4>{getText("singUp")}</h4>
      <div className="input-container">
        <input
          type="text"
          id="nameInput"
          placeholder=" "
          aria-label="name"
          minLength={2}
          maxLength={35}
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
        <label htmlFor="nameInput">{getText("userNameInputLabel")} *</label>
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
        <label htmlFor="emailInput">{getText("emailInputLabel")} *</label>
      </div>

      <div className="input-container">
        <input
          type={isPasswordVisible ? "text" : "password"}
          id="passwordInput"
          placeholder=" "
          minLength={6}
          maxLength={12}
          aria-label="Password"
          required
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <div
          onMouseDown={() => togglePasswordVisibility(1)}
          onMouseUp={() => togglePasswordVisibility(1)}
          className="toggle-password-btn"
        >
          {isPasswordVisible ? (
            <FontAwesomeIcon icon={faEye} />
          ) : (
            <FontAwesomeIcon icon={faEyeSlash} />
          )}
        </div>
        <label htmlFor="passwordInput">{getText("passwordInputLabel")} *</label>
      </div>

      <div className="input-container">
        <input
          type={isSecondPasswordVisible ? "text" : "password"}
          id="secondPasswordInput"
          placeholder=" "
          minLength={6}
          maxLength={12}
          aria-label="secondPassword"
          required
          value={secondPassword}
          onChange={(e) => setSecondPassword(e.target.value)}
        />
        <div
          onMouseDown={() => togglePasswordVisibility(2)}
          onMouseUp={() => togglePasswordVisibility(2)}
          className="toggle-password-btn"
        >
          {isSecondPasswordVisible ? (
            <FontAwesomeIcon icon={faEye} />
          ) : (
            <FontAwesomeIcon icon={faEyeSlash} />
          )}
        </div>
        <label htmlFor="secondPasswordInput">
          {getText("secondPasswordInputLabel")} *
        </label>
      </div>

      <button
        onSubmit={handleSubmit}
        className={validateSubmoit ? "" : "submit"}
        type="submit"
        disabled={validateSubmoit}
      >
        {getText("submit")}
      </button>
    </div>
  );
};
