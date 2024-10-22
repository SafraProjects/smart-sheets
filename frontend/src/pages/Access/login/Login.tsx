import { faEye, faEyeSlash } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useLanguage } from "../../../../contexts/languageContext";
import { UserLogin } from "../../../../interface/user.dtos";
import { Alert } from "../../../../modules/alert/Alert";
import { login } from "../../../API/axios/axiosCenteral";
import validateEmail from "../../../utils/validetEmail";
import "./login.css";
import { Loader } from "../../../../modules/loader/Loader";

export const Login: React.FC = () => {
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [alertMessage, setAlertMessage] = useState<string>("ארעה שגיאה");
  const [isPasswordVisible, setIsPasswordVisible] = useState(false);
  const [alert, setAlert] = useState<boolean>(false);
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
    nav("/auto/verify/sendPassword/" + email);
  };
  const handelNavigationToSingUp = () => {
    nav("/auto/sing-up");
  };

  useEffect(() => {
    if (email.includes("@") && email.includes(".") && password) {
      const emailValidation = validateEmail(email);
      console.log(">>> valid:");
      setFormValidEmail((prev) => ({
        ...prev,
        isValid: emailValidation.isValid,
        message: getText("alertEmailMessage"),
        email: emailValidation.suggestion ? emailValidation.suggestion : "",
      }));
    } else if (email && password) {
      const emailValidation = validateEmail(email);
      setFormValidEmail((prev) => ({
        ...prev,
        isValid: false,
        message: "תחביר שגוי: חסרים סימני מפתח כגון @ או נקודה",
        email: "",
      }));
    }
    if (email.length === 0) {
      setFormValidEmail((prev) => ({
        ...prev,
        isValid: true,
        message: "",
        email: "",
      }));
    }
  }, [email, password]);

  const handleSubmit = async () => {
    const userToDb: UserLogin = {
      email: email,
      password: password,
    };

    try {
      setAlert(false);
      setIsLoading(true);

      const user = await login(userToDb);
      console.log("user data:  ", user);
      if (user) {
        nav("/user");
      }
    } catch (error) {
      setAlertMessage("ארעה שגיאה");
      if (error instanceof Error) {
        if (error.message.includes("Internal Server Error")) {
          setAlertMessage("המשתמש אינו קיים מערכת");
        } else if (error.message.includes("Bad Request")) {
          setAlertMessage("סיסמא שגויה");
        }
      }
      console.error("Error during sign up:", error);

      setAlert(true);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <form>
        {!isLoading && (
          <>
            <h2>{getText("login")}</h2>
            <div className="input-container">
              <input
                className={
                  "input " + (formValidEmail.isValid ? "" : "un-valid")
                }
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
                className="input"
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
              {getText("confirm")}
            </button>
          </>
        )}
        <Loader isOpen={isLoading} />
      </form>
      <Alert
        isOpen={!formValidEmail.isValid && email.length > 15}
        type="error"
        position="top"
        message={formValidEmail.message}
        mainMessage={formValidEmail.email}
        func={formValidEmail.email !== "" ? handelFixEmail : undefined}
        funcMessage={getText("yes")}
      />
      <Alert
        isOpen={alert}
        closeButton={true}
        type="error"
        position="top"
        message={alertMessage}
      />
    </>
  );
};
