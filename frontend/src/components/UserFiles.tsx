import React, { useState } from "react";
import { Table } from "./Table";
import { FilesTabs } from "./FilesTabs";
import "./componentStyle.css";
import {
  faRectangleList,
  faTableList,
} from "@fortawesome/free-solid-svg-icons";

export const UserFiles: React.FC = () => {
  const [isTableCreated, setIsTableCreated] = useState<boolean>(false);
  return (
    <div className="user-files">
      <FilesTabs />
      <div className="table-area">
        {isTableCreated ? <Table /> : <div className="table"></div>}
      </div>
    </div>
  );
};
