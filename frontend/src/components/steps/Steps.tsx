import React, { useState } from "react";
import "./steps.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCaretLeft, faCaretRight } from "@fortawesome/free-solid-svg-icons";

interface StepsProps {
  steps: React.ReactNode[]; // התוכן לכל צעד (מוגדר מבחוץ)
  isSelected: boolean;
}

export const Steps: React.FC<StepsProps> = ({ steps, isSelected }) => {
  const [currentStepIndex, setCurrentStepIndex] = useState<number>(0);

  const handleNext = () => {
    if (canGoNext) {
      setCurrentStepIndex(currentStepIndex + 1);
    }
  };

  const handlePrev = () => {
    if (canGoPrev) {
      setCurrentStepIndex(currentStepIndex - 1);
    }
  };

  const canGoNext = currentStepIndex < steps.length - 1 && isSelected;
  const canGoPrev = currentStepIndex > 0 && isSelected;

  return (
    <div className="step">
      <div className={`prev ${canGoPrev ? "active" : ""}`} onClick={handlePrev}>
        <FontAwesomeIcon icon={faCaretLeft} />
      </div>
      <div className="step-content">{steps[currentStepIndex]}</div>

      <div className={`prev ${canGoNext ? "active" : ""}`} onClick={handleNext}>
        <FontAwesomeIcon icon={faCaretRight} />
      </div>
    </div>
  );
};
