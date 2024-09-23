import React from "react";
import { Table } from "./Table";
import { FilesTabs } from "./FilesTabs";

export const UserFiles: React.FC = () => {
  return (
    <div className="user-files">
      <FilesTabs />
      <div className="table-area">
        <Table />
      </div>
    </div>
  );
};
