import React from "react";
import "./Dialog.css";

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  children: React.ReactNode;
  selected: boolean;
}

const Modal: React.FC<ModalProps> = ({
  isOpen,
  onClose,
  children,
  selected,
}) => {
  return (
    <div className={`modal ${isOpen ? "open" : "close"}`} onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <button className="close-button" onClick={onClose}>
            &times;
          </button>
        </div>
        <div className="modal-body">{children}</div>
        <div className="modal-fote">
          <button onClick={onClose}>close</button>
          {selected && <button onClick={onClose}>next</button>}
        </div>
      </div>
    </div>
  );
};

export default Modal;
