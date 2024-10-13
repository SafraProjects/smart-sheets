import { faEye, faEyeSlash, faL } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useEffect, useState } from "react";
import { useLanguage } from "../../../../contexts/languageContext";
import { UserSignInDto } from "../../../../interface/user.dtos";
import { singIn } from "../../../API/axios/axiosCenteral";
import { useNavigate } from "react-router-dom";
import validateEmail from "../../../utils/validetEmail";
import { Alert } from "../../../../modules/alert/Alert";
import { Alerts } from "../../../../modules/alert/alerts";

export const SingUp: React.FC = () => {
  const [name, setName] = useState<string>("");
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [secondPassword, setSecondPassword] = useState<string>("");
  const [isPasswordVisible, setIsPasswordVisible] = useState(false);
  const [isSecondPasswordVisible, setIsSecondPasswordVisible] = useState(false);
  const [isLoding, setIsLoding] = useState<boolean>(false);
  const [formState, setFormState] = useState({
    email: "",
    emailValid: true,
    emailMessage: "",
    password: true,
    // סטטוס של הסיסמא
  });

  const { getText } = useLanguage();
  const nav = useNavigate();

  const togglePasswordVisibility = (num: number) => {
    if (num === 1) {
      setIsPasswordVisible(!isPasswordVisible);
    } else {
      setIsSecondPasswordVisible(!isSecondPasswordVisible);
    }
  };

  // הוספת קובץ עם פונקציות אימות מייל!!!
  let unValidSubmit: boolean =
    password.length < 6 ||
    secondPassword.length < password.length ||
    (!email.includes("@") && !email.includes(".")) ||
    !name;

  const handelEmailFixed = () => {
    setEmail(formState.email);
  };

  useEffect(() => {
    if (!unValidSubmit) {
      const emailValidation = validateEmail(email);
      setFormState((prev) => ({
        ...prev,
        email: emailValidation.suggestion ? emailValidation.suggestion : "",
        emailValid: emailValidation.isValid,
        emailMessage: emailValidation.message,
        password: !(password !== secondPassword),
      }));
      unValidSubmit = true;
    }
  }, [unValidSubmit, email, password, secondPassword]);

  const handleSubmit = async () => {
    console.log(">> submit");

    const userToDb: UserSignInDto = {
      name: name,
      email: email,
      password: password,
    };

    try {
      setIsLoding(true);
      const a = await singIn(userToDb);
      console.log("message: ", a.message);
    } catch (error) {
      console.error("Error during sign up:", error);
    } finally {
      setIsLoding(false);
      nav("/auto/verify-email/wait");
    }
  };

  return (
    <>
      <form>
        {!isLoding ? (
          <>
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
              <label htmlFor="nameInput">
                {getText("userNameInputLabel")} *
              </label>
            </div>
            <div className="input-container">
              <input
                className={formState.emailValid ? "" : "un-valid"}
                type="email"
                id="emailInput"
                placeholder=" "
                aria-label="Email"
                maxLength={50}
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                autoComplete="new-email"
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
                autoComplete="new-password"
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
              <label htmlFor="passwordInput">
                {getText("passwordInputLabel")} *
              </label>
            </div>
            <div className="input-container">
              <input
                type={isSecondPasswordVisible ? "text" : "password"}
                className={formState.password ? "" : "un-valid"}
                id="secondPasswordInput"
                placeholder=" "
                minLength={6}
                maxLength={12}
                aria-label="secondPassword"
                required
                value={secondPassword}
                onChange={(e) => setSecondPassword(e.target.value)}
                autoComplete="new-password"
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
              onClick={handleSubmit}
              className={`btn-submit ${unValidSubmit ? "" : "submit"}`}
              type="submit"
              disabled={unValidSubmit}
            >
              {getText("submit")}
            </button>{" "}
          </>
        ) : (
          <>
            <h3>רושם...</h3>
            <div className="loader"></div>
          </>
        )}
      </form>

      <Alert
        isOpen={!formState.emailValid}
        type="error"
        func={handelEmailFixed}
        funcMessage="אשר"
        message={formState.emailMessage}
      />
      <Alert
        isOpen={formState.emailValid && !formState.password}
        type="error"
        message={"הסיסמאות אינן תואמות"}
      />
    </>
  );
};
