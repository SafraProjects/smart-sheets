import React, { useState } from "react";
import "./steps.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCaretLeft, faCaretRight } from "@fortawesome/free-solid-svg-icons";

interface StepsProps {
  classSize: number;
  steps: React.ReactNode[]; // התוכן לכל צעד (מוגדר מבחוץ)
  isSelected: boolean;
  numOfSteps: number;
}

export const Steps: React.FC<StepsProps> = ({
  steps,
  isSelected,
  classSize,
  numOfSteps,
}) => {
  const [currentStepIndex, setCurrentStepIndex] = useState<number>(0);
  const [rapClassSize, setrapClassSize] = useState<string>(
    classSize === 250 ? "rap-flx-250-350" : "rap-flx-200-300"
  );

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
      <div className="step-content">
        <div className={rapClassSize}>{steps[currentStepIndex]}</div>
        <div className="dots">
          {Array.from({ length: numOfSteps }, (_, index) => (
            <div
              className={`dot ${index + 1 === 2 ? "active" : ""}`}
              key={index}
            ></div>
          ))}
        </div>
      </div>

      <div className={`prev ${canGoNext ? "active" : ""}`} onClick={handleNext}>
        <FontAwesomeIcon icon={faCaretRight} />
      </div>
    </div>
  );
};
