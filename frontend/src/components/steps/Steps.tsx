import React, { useEffect, useState } from "react";
import "./steps.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCaretLeft, faCaretRight } from "@fortawesome/free-solid-svg-icons";

interface StepsProps {
  classSize: number;
  steps: React.ReactNode[]; // התוכן לכל צעד (מוגדר מבחוץ)
  optionSelected: string | null;
  numOfSteps: number;
}

export const Steps: React.FC<StepsProps> = ({
  steps,
  optionSelected,
  classSize,
  numOfSteps,
}) => {
  const [currentStepIndex, setCurrentStepIndex] = useState<number>(0);
  const [Steps, setSteps] = useState<React.ReactNode[]>(steps);
  useEffect(() => {
    if (optionSelected) {
      if (optionSelected === "upload file") {
        setSteps(steps.filter((_, index) => index % 2 === 0));
      } else {
        setSteps(steps.filter((_, index) => index === 0 || index % 2 !== 0));
      }
    }
  }, [optionSelected]);

  const canGoNext = currentStepIndex < Steps.length - 1 && !!optionSelected;
  const canGoPrev = currentStepIndex > 0 && !!optionSelected;

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

  return (
    <div className="step">
      <div className={`prev ${canGoPrev ? "active" : ""}`} onClick={handlePrev}>
        <FontAwesomeIcon icon={faCaretLeft} />
      </div>
      <div className="step-content">
        <div className={"rap-flx-" + classSize}>
          <div className="rap-step">{Steps[currentStepIndex]}</div>
        </div>
        <div className="steps-dots">
          {Array.from({ length: numOfSteps }, (_, index) => (
            <div
              className={`dot ${index === currentStepIndex ? "active" : ""}`}
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
