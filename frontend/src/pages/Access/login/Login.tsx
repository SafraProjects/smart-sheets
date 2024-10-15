import React, { useEffect, useState } from "react";
import { useLanguage } from "../../../../contexts/languageContext";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faEye, faEyeSlash } from "@fortawesome/free-solid-svg-icons";
import { useNavigate } from "react-router-dom";
import { login } from "../../../API/axios/axiosCenteral";
import { UserDBDto, UserLogin } from "../../../../interface/user.dtos";
import validateEmail from "../../../utils/validetEmail";
import "./login.css";
import { Alert } from "../../../../modules/alert/Alert";

export const Login: React.FC = () => {
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [isPasswordVisible, setIsPasswordVisible] = useState(false);
  const [formValidEmail, setFormValidEmail] = useState({
    isValid: true,
    message: "",
    email: "",
  });
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const validateLoginSubmit = formValidEmail.isValid && password.length > 5;

  const nav = useNavigate();
  const { getText } = useLanguage();

  const handelFixEmail = () => {
    setEmail(formValidEmail.email);
    setFormValidEmail({
      isValid: true,
      message: "",
      email: "",
    });
  };

  const togglePasswordVisibility = () => {
    setIsPasswordVisible(!isPasswordVisible);
  };

  const handelRecreatePassword = () => {
    nav("/auto/verify/create-code");
  };
  const handelNavigationToSingUp = () => {
    nav("/auto/sing-up");
  };

  useEffect(() => {
    if (email.includes("@") && email.includes(".")) {
      console.log(">>> valid:");
      const emailValidation = validateEmail(email);
      setFormValidEmail((prev) => ({
        ...prev,
        isValid: emailValidation.isValid,
        message: emailValidation.message ? emailValidation.message : "",
        email: emailValidation.suggestion ? emailValidation.suggestion : "",
      }));
    }
  }, [email]);

  const handleSubmit = async () => {
    const userToDb: UserLogin = {
      email: email,
      password: password,
    };
    try {
      // console.log(userToDb);
      setIsLoading(true);
      const user: UserDBDto = await login(userToDb);

      nav("/user");
      console.log("user data:  ", user);

      throw new Error("Unexpected response structure");
    } catch (error) {
      console.error("Error during sign up:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <form>
        {!isLoading ? (
          <>
            <h2>{getText("login")}</h2>
            <div className="input-container">
              <input
                className={formValidEmail.isValid ? "" : "un-valid"}
                type="email"
                id="emailInput"
                placeholder=""
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
            {email && (
              <div
                className="recreate-password"
                onClick={handelRecreatePassword}
              >
                {getText("recreatePassword")}
              </div>
            )}
            <div
              className="recreate-password"
              onClick={handelNavigationToSingUp}
            >
              {/* {getText("recreatePassword")} */}
              {getText("createAccount")}
            </div>

            <button
              onClick={handleSubmit}
              className={`btn-submit ${!validateLoginSubmit ? "" : "submit"}`}
              type="submit"
              disabled={!validateLoginSubmit}
            >
              {getText("submit")}
            </button>
          </>
        ) : (
          <>
            {/* make a component from the loader !!! */}
            <h3>רושם...</h3>
            <div className="loader"></div>
          </>
        )}
      </form>
      <Alert
        isOpen={!formValidEmail.isValid && email.length > 8}
        type="error"
        position="top"
        message={formValidEmail.message}
        mainMessage={formValidEmail.email}
        func={handelFixEmail}
        funcMessage="אישור"
      />
    </>
  );
};
