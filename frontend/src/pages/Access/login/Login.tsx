import React, { useState } from "react";
import { useLanguage } from "../../../../contexts/languageContext";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faEye, faEyeSlash } from "@fortawesome/free-solid-svg-icons";
import { useNavigate } from "react-router-dom";
import { login } from "../../../API/axios/axiosCenteral";
import { UserDBDto, UserLogin } from "../../../../interface/user.dtos";

export const Login: React.FC = () => {
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [isPasswordVisible, setIsPasswordVisible] = useState(false);
  const [isLoding, setIsloding] = useState<boolean>(false);

  const nav = useNavigate();
  const { getText } = useLanguage();

  const togglePasswordVisibility = () => {
    setIsPasswordVisible(!isPasswordVisible);
  };

  const handelRecreatePassword = () => {};

  const handleSubmit = async () => {
    console.log(">>>>>>>>>>>>>>");
    const userToDb: UserLogin = {
      email: email,
      password: password,
    };
    try {
      // console.log(userToDb);
      setIsloding(true);
      const user: UserDBDto = await login(userToDb);

      nav("/user");
      console.log("user data:  ", user);

      throw new Error("Unexpected response structure");
    } catch (error) {
      console.error("Error during sign up:", error);
    } finally {
      setIsloding(false);
    }
  };

  return (
    <>
      <form>
        {!isLoding ? (
          <>
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

              <label htmlFor="passwordInput">
                {getText("passwordInputLabel")} *
              </label>
              <div
                onMouseDown={togglePasswordVisibility}
                onMouseUp={togglePasswordVisibility}
                className="toggle-password-btn"
              >
                {isPasswordVisible ? (
                  <FontAwesomeIcon icon={faEye} />
                ) : (
                  <FontAwesomeIcon icon={faEyeSlash} />
                )}
              </div>
            </div>
            <div className="recreate-password" onClick={handelRecreatePassword}>
              {getText("recreatePassword")}
            </div>
            <button
              onClick={handleSubmit}
              className={`btn-submit ${!email || !password ? "" : "submit"}`}
              type="submit"
              disabled={!email || !password}
            >
              {getText("submit")}
            </button>
          </>
        ) : (
          <>
            <h3>רושם...</h3>
            <div className="loader"></div>
          </>
        )}
      </form>
    </>
  );
};
