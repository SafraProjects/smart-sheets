import {
  faFileUpload,
  faPlus,
  faTableList,
  faTimes,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useState } from "react";
import { useLanguage } from "../../contexts/languageContext";
import { filesTabs, randomFilesInterface } from "../utils/randomData";
import Modal from "../../modules/dialog/Dialog";
import { Steps } from "../../modules/steps/Steps";

export const FilesTabs: React.FC = () => {
  const [tabs, setTabs] = useState<randomFilesInterface[]>(filesTabs);
  const [activeTab, setActiveTab] = useState<number>(1);
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const [tableOptionSelected, setTableOptionSelected] = useState<string | null>(
    null
  );
  const { getText } = useLanguage();

  const handleOpen = () => {
    setIsOpen(true);
    // handleAddTab();
  };
  const handleClose = () => setIsOpen(false);

  const onCloseTab = (id: number) => {
    const updatedTabs = tabs.filter((tab) => tab.id !== id);
    const tabIndex = tabs.findIndex((tab) => tab.id === id) - 1;
    setTabs(updatedTabs);
    if (activeTab === id && updatedTabs.length > 0) {
      setActiveTab(tabIndex > 0 ? tabs[tabIndex].id : updatedTabs[0].id);
    }
  };

  const handleAddTab = () => {
    if (isOpen === false) {
      let newId = tabs.length > 0 ? tabs[tabs.length - 1].id + 1 : 1;
      setTabs([
        ...tabs,
        {
          id: newId,
          name: `file-${newId}`,
          content: `file-${newId}-content`,
        },
      ]);
      setActiveTab(newId);
    }
  };

  // list of add file or create table steps for steps component
  const steps = [
    <>
      <h2>{getText("tableTitle")}</h2>
      <div
        onClick={() => setTableOptionSelected("upload file")}
        id="option"
        className={`add-file ${
          tableOptionSelected === "upload file" ? "selected" : ""
        }`}
      >
        <h4>{getText("uploadedFile")}</h4>
        <div className="add-file-icon">
          <FontAwesomeIcon icon={faFileUpload}></FontAwesomeIcon>
        </div>
      </div>
      <div
        onClick={() => setTableOptionSelected("create table")}
        id="option"
        className={`add-file ${
          tableOptionSelected === "create table" ? "selected" : ""
        }`}
      >
        <h4>{getText("createTable")}</h4>
        <div className="add-file-icon">
          <FontAwesomeIcon icon={faTableList}></FontAwesomeIcon>
        </div>
      </div>
    </>,
    <>
      <div className="add-file-select">
        <div>cr2</div>
      </div>
    </>,
    <>
      <div className="add-file-select">
        <div>up2</div>
      </div>
    </>,
    <>
      <div className="add-file-select">
        <div>cr3</div>
      </div>
    </>,
    <>
      <div className="add-file-select">
        <div>up3</div>
      </div>
    </>,
  ];

  return (
    <div className="tab-files-area" role="tablist">
      {tabs.map((tab) => (
        <div
          key={tab.id}
          onClick={() => setActiveTab(tab.id)}
          className={`tab-file  ${activeTab === tab.id ? "active" : ""}`}
          role="tab"
          aria-selected={activeTab === tab.id}
        >
          <div
            className="btn-close-tab"
            onClick={(e) => {
              e.stopPropagation();
              onCloseTab(tab.id);
            }}
          >
            <FontAwesomeIcon icon={faTimes} />
          </div>
          <span>{tab.name}</span>
        </div>
      ))}
      <button
        className="btn-add-file"
        onClick={() => handleOpen()}
        title="הוספת קובץ"
      >
        <FontAwesomeIcon icon={faPlus} />
      </button>

      <Modal isOpen={isOpen} onClose={handleClose}>
        <Steps
          steps={steps}
          numOfSteps={3}
          classSize={250}
          optionSelected={tableOptionSelected}
          updateOptionSelect={setTableOptionSelected}
        />
      </Modal>
    </div>
  );
};
