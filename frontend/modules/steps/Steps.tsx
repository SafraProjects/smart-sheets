import React, { useEffect, useState } from "react";
import "./steps.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCaretLeft, faCaretRight } from "@fortawesome/free-solid-svg-icons";

interface StepsProps {
  steps: React.ReactNode[]; // התוכן לכל צעד (מוגדר מבחוץ)
  numOfSteps?: number;
  classSize?: number;
  optionSelected?: string | null;
  updateOptionSelect?: (setOptionSelected: string | null) => void | undefined;
}

export const Steps: React.FC<StepsProps> = ({
  steps,
  numOfSteps,
  classSize,
  optionSelected,
  updateOptionSelect,
}) => {
  const [currentStepIndex, setCurrentStepIndex] = useState<number>(0);
  const [direction, setDirection] = useState<"next" | "prev" | null>(null);
  const [transitioning, setTransitioning] = useState(false);
  const [Steps, setSteps] = useState<React.ReactNode[]>(steps);

  const canGoNext =
    currentStepIndex < Steps.length - 1 &&
    (currentStepIndex === 0 && optionSelected !== undefined
      ? !!optionSelected
      : true);

  const canGoPrev =
    currentStepIndex > 0 &&
    (currentStepIndex === 0 && optionSelected !== undefined
      ? !!optionSelected
      : true);

  const stepsLength = numOfSteps ? numOfSteps : steps.length;

  useEffect(() => {
    if (transitioning) {
      const timer = setTimeout(() => {
        setDirection(null);
        setTransitioning(false);
      }, 500);
      return () => clearTimeout(timer);
    }
  }, [transitioning]);

  useEffect(() => {
    if (optionSelected && currentStepIndex === 0) {
      if (optionSelected === "upload file") {
        setSteps(steps.filter((_, index) => index % 2 === 0));
      } else {
        setSteps(steps.filter((_, index) => index === 0 || index % 2 !== 0));
      }
    }
  }, [optionSelected]);

  // const handelCloseOptionSelect = () => {
  //   if (optionSelected && updateOptionSelect) {
  //     updateOptionSelect(null);
  //   }
  // };

  const handleNext = () => {
    // handelCloseOptionSelect();
    if (canGoNext && !transitioning) {
      setDirection("next");
      setTransitioning(true);
      setTimeout(() => {
        setCurrentStepIndex((prev) => prev + 1);
      }, 500);
    }
  };

  const handlePrev = () => {
    if (canGoPrev && !transitioning) {
      setDirection("prev");
      setTransitioning(true);
      setTimeout(() => {
        setCurrentStepIndex((prev) => prev - 1);
      }, 500);
    }
  };

  return (
    <div className="step">
      <div className={`prev ${canGoPrev ? "active" : ""}`} onClick={handlePrev}>
        <FontAwesomeIcon icon={faCaretLeft} />
      </div>
      <div className="step-content">
        <div className={"rap-flx-" + (classSize ? classSize : 200)}>
          <div
            className={
              "rap-step " +
              (direction
                ? direction === "prev"
                  ? "exit-right"
                  : "exit-left"
                : "")
            }
          >
            {Steps[currentStepIndex]}
          </div>

          {direction && (
            <div
              className={
                "rap-step " +
                (direction === "next" ? "enter-right" : "enter-left")
              }
            >
              {Steps[currentStepIndex + (direction === "next" ? 1 : -1)]}
            </div>
          )}
        </div>
        <div className="steps-dots">
          {Array.from({ length: stepsLength }, (_, index) => (
            <div
              className={`dot ${index === currentStepIndex ? "active" : ""}`}
              key={index}
            ></div>
          ))}
        </div>
      </div>

      <div className={`next ${canGoNext ? "active" : ""}`} onClick={handleNext}>
        <FontAwesomeIcon icon={faCaretRight} />
      </div>
    </div>
  );
};
