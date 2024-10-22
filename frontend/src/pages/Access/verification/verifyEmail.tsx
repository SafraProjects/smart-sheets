import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import logo from "../../../../assets/tabio.png";
import { useLanguage } from "../../../../contexts/languageContext";
import { Loader } from "../../../../modules/loader/Loader";
import {
  recreatePassword,
  resendVerificationEmail,
  sendPasswordToUser,
  verifyEmail,
  verifyPassword,
} from "../../../API/axios/axiosCenteral";
import "./verifyemail.css";

export const Verify: React.FC = () => {
  const [isVerify, setIsVerify] = useState<boolean>(false);
  const [expire, setExpire] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [userForm, setUserForm] = useState<{
    email: string;
    token: string;
    value: string;
  }>({ email: "", token: "", value: "" });
  const [password, setPassword] = useState<string>("");
  const { getText } = useLanguage();
  const nav = useNavigate();
  const { email, value } = useParams();
  const [isMounted, setIsMounted] = useState<boolean>(false);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  useEffect(() => {
    if (isMounted) {
      const newUserForm = {
        email: email || "",
        token:
          value === "waite" ||
          value === "sendPassword" ||
          value === "verifyPassword" ||
          value === "resendEmail"
            ? ""
            : value || "",
        value: value || "",
      };
      setUserForm(newUserForm);
    }
  }, [isMounted]);

  // שליחת סיסמה למייל המשתמש
  useEffect(() => {
    const sendPasswordToUserEmail = async () => {
      if (userForm.email && userForm.value === "sendPassword") {
        setIsLoading(true);
        try {
          const response = await sendPasswordToUser(userForm.email);
          if (response) {
            setUserForm((prev) => ({
              ...prev,
              value: "verifyPassword",
            }));
            nav("/auto/verify/verifyPassword/" + userForm.email);

            console.log(response);
          }
        } catch (error) {
          handleEmailError(error);
        } finally {
          setIsLoading(false);
        }
      }
    };

    sendPasswordToUserEmail();
  }, [userForm.value]);

  // אימות כתובת המייל
  useEffect(() => {
    const emailVerification = async () => {
      if (userForm.token) {
        setIsLoading(true);
        try {
          const response = await verifyEmail(userForm.token);
          setIsVerify(response !== undefined);
          setTimeout(() => nav("/auto/log-in"), 5000);
        } catch (error) {
          handleEmailError(error);
        } finally {
          setIsLoading(false);
        }
      }
    };

    emailVerification();
  }, [userForm.token]);

  // פונקציה לטיפול בשגיאות אימייל
  const handleEmailError = (error: unknown) => {
    if (error instanceof Error) {
      if (error.message.includes("Unauthorized")) {
        setExpire(true);
      } else if (error.message.includes("Bad Request")) {
        setIsVerify(true);
        setTimeout(() => nav("/auto/log-in"), 5000);
      }
    } else {
      console.error("Unknown error format", error);
    }
  };

  const handleResendEmail = async () => {
    if (userForm.email || email) {
      setIsLoading(true);
      try {
        const message = await resendVerificationEmail(
          userForm.email ? userForm.email : (email as string)
        );
        if (message) {
          setUserForm({
            value: "waite",
            email: "",
            token: "",
          });
          setExpire(false);
          nav("/auto/verify/waite");
        }
      } catch (error) {
        console.error("some error:::", error);
      } finally {
        setIsLoading(false);
      }
    }
  };

  const handleVerifyEmailPassword = async () => {
    if (password.length === 4) {
      setIsLoading(true);
      try {
        await verifyPassword({ email: userForm.email, password: password });
        setUserForm((prev) => ({
          ...prev,
          value: "newPassword",
        }));
        setPassword("");
        nav("/auto/verify/newPassword/" + userForm.email);
      } catch (error) {
        console.error("some error:::", error);
      } finally {
        setIsLoading(false);
      }
    }
  };

  const handleChangePassword = async () => {
    setIsLoading(true);
    try {
      const response = await recreatePassword({
        email: userForm.email,
        password: password,
      });
      setIsVerify(response !== undefined);
      setTimeout(() => nav("/auto/log-in"), 5000);
    } catch (error) {
      console.error("some error:::", error);
    } finally {
      setIsLoading(false);
    }
  };

  // הצגת טקסט ההודעות למשתמש
  const renderVerificationText = (message: string) =>
    message.split("\n").map((text, index) => (
      <React.Fragment key={index}>
        {text}
        <br />
      </React.Fragment>
    ));

  // הצגת הודעות בהתאם למצב הנוכחי
  const renderVerificationMessage = () => {
    if (isLoading) return <Loader isOpen={isLoading} />;

    if (isVerify) {
      return (
        <div className="verification-email">
          {renderVerificationText(getText("verifyEmailMessage"))}
        </div>
      );
    }

    if (expire) {
      return (
        <div className="verification-email">
          {renderVerificationText(getText("expireVerificationTokenMessage"))}
          <div onClick={() => handleResendEmail()} className="btn-send-email">
            <div className="send-email-btn-text">{getText("resend")}</div>
          </div>
        </div>
      );
    }

    if (userForm.value === "waite") {
      return (
        <div className="verification-email">
          {renderVerificationText(getText("EmailSandMessage"))}
        </div>
      );
    }

    if (userForm.value === "verifyPassword") {
      return (
        <div className="verification-email">
          {renderVerificationText(getText("SandPasswordToEmailMessage"))}
          <input
            id="passwordSend"
            type="text"
            className="input"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <input
            type="submit"
            onClick={handleVerifyEmailPassword}
            className={"btn-submit " + (password.length === 4 ? "submit" : "")}
            disabled={password.length !== 4}
          />
        </div>
      );
    }

    if (userForm.value === "newPassword") {
      return (
        <div className="verification-email">
          <div className="create-new-password">
            {"צור סיסמא חדשה"}
            <input
              id="passwordSend2"
              type="text"
              minLength={6}
              maxLength={12}
              value={password}
              className="input"
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <input
              type="submit"
              onClick={handleChangePassword}
              className={"btn-submit " + (password.length > 5 ? "submit" : "")}
              disabled={password.length < 6}
            />
          </div>
        </div>
      );
    }

    return null;
  };

  return (
    <div className="log-back">
      <div className="verification-area">
        <img src={logo} alt="tabio logo" width="140px" height="50px" />
        {renderVerificationMessage()}
      </div>
    </div>
  );
};
