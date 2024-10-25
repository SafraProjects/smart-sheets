import React, { useState } from "react";
import { useLanguage } from "../../../../contexts/languageContext";

export const RecreatePassword: React.FC = () => {
  const [password, setPassword] = useState<string>("");
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const { getText } = useLanguage();

  const handleSubmit = () => {
    //  await
  };

  return (
    <div className="recreate-password-area">
      <div className="input-container">
        <input
          className="input"
          type={"password"}
          id="passwordInput"
          placeholder=" "
          minLength={4}
          maxLength={4}
          aria-label="Password"
          required
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <label htmlFor="passwordInput">{getText("passwordInputLabel")} *</label>
      </div>

      <button
        onClick={handleSubmit}
        className={`btn-submit ${password.length < 4 ? "" : "submit"}`}
        type="submit"
        disabled={password.length < 4}
      >
        {getText("confirm")}
      </button>
    </div>
  );
};
