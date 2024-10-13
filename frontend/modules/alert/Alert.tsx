import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faExclamationCircle,
  faInfoCircle,
  faCheckCircle,
  faExclamationTriangle,
} from "@fortawesome/free-solid-svg-icons";
import "./Alert.css";

interface AlertProp {
  isOpen: boolean;
  type?: "error" | "info" | "success" | "warning";
  position?: "top" | "bottom" | "left" | "right";
  mainMessage?: string;
  message: string;
  func?: () => void;
  funcMessage?: string;
}

export const Alert: React.FC<AlertProp> = ({
  isOpen = false,
  type = "info",
  position = "top",
  mainMessage,
  message = "write a message",
  func,
  funcMessage,
}) => {
  if (!isOpen) return null;

  return (
    <div className={`alert-container ${position}`}>
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
        {mainMessage && (
          <span className="alert-main-message">{mainMessage}</span>
        )}
        <span className="alert-message">{message}</span>
      </div>
      {func && funcMessage && (
        <div className="button-alert" onClick={func}>
          {funcMessage}
        </div>
      )}
    </div>
  );
};
