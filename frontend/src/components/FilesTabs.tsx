import React, { useState } from "react";
import { filesTabs, randomFilesInterface } from "./randomData";

export const FilesTabs: React.FC = () => {
  const [tabs, setTabs] = useState<randomFilesInterface[]>(filesTabs);
  const [activeTab, setActiveTab] = useState<number>();

  const onCloseTab = (id: number) => {
    const updatedTabs = tabs.filter((tab) => tab.id !== id);
    setTabs(updatedTabs);
    if (activeTab === id && updatedTabs.length > 0) {
      setActiveTab(updatedTabs[0].id);
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
            x
          </div>
          <span>{tab.name}</span>
        </div>
      ))}
      <button className="btn-add-file" onClick={() => handleAddTab()}>
        +
      </button>
    </div>
  );
};
