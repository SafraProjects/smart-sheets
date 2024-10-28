import React, { useState, useEffect } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faExclamationCircle,
  faInfoCircle,
  faCheckCircle,
  faExclamationTriangle,
  faTimes,
} from "@fortawesome/free-solid-svg-icons";
import "./Alert.css";

interface AlertProp {
  isOpen: boolean;
  closeButton?: boolean;
  closeAt?: number;
  type?: "error" | "info" | "success" | "warning";
  position?: "top" | "bottom" | "left" | "right";
  mainMessage?: string;
  message?: string;
  func?: () => void;
  funcMessage?: string;
}

export const Alert: React.FC<AlertProp> = ({
  isOpen,
  closeButton,
  closeAt,
  type = "info",
  position = "top",
  mainMessage,
  message = "write a message",
  func,
  funcMessage,
}) => {
  const [timeOut, setTimeOut] = useState<boolean>(false);

  const handelClose = () => {
    setTimeOut(true);
  };

  useEffect(() => {
    if (isOpen) {
      setTimeOut(false);
    }
  }, [isOpen]);

  useEffect(() => {
    if (closeAt && isOpen) {
      setTimeOut(false);
      const timer = setTimeout(() => setTimeOut(true), closeAt * 1000);
      return () => clearTimeout(timer);
    }
  }, [isOpen, closeAt]);

  if (!isOpen || timeOut) return null;

  return (
    <div className={`alert-container ${position}`}>
      {func && funcMessage && (
        <div className="button-alert" onClick={func}>
          {funcMessage}
        </div>
      )}
      <div className={`alert ${type}`}>
        <FontAwesomeIcon
          icon={
            type === "error"
              ? faExclamationCircle
              : type === "info"
              ? faInfoCircle
              : type === "success"
              ? faCheckCircle
              : faExclamationTriangle
          }
        />
        {message && <span className="alert-message">{message}</span>}
        {mainMessage && (
          <span className="alert-main-message">{mainMessage}</span>
        )}
        {closeButton && (
          <span className="close-alert" onClick={handelClose}>
            <FontAwesomeIcon icon={faTimes} />
          </span>
        )}
      </div>
    </div>
  );
};
