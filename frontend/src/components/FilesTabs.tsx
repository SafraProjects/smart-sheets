import { faPlus, faTimes } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useState } from "react";
import { filesTabs, randomFilesInterface } from "../utils/randomData";

export const FilesTabs: React.FC = () => {
  const [tabs, setTabs] = useState<randomFilesInterface[]>(filesTabs);
  const [activeTab, setActiveTab] = useState<number>(1);

  const onCloseTab = (id: number) => {
    const updatedTabs = tabs.filter((tab) => tab.id !== id);
    const tabIndex = tabs.findIndex((tab) => tab.id === id) - 1;
    setTabs(updatedTabs);
    if (activeTab === id && updatedTabs.length > 0) {
      setActiveTab(tabIndex > 0 ? tabs[tabIndex].id : updatedTabs[0].id);
    }
  };

  const handleAddTab = () => {
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
  };

  return (
    <div className="tab-files-area">
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
        onClick={() => handleAddTab()}
        title="הוספת קובץ"
      >
        <FontAwesomeIcon icon={faPlus} />
      </button>
    </div>
  );
};
