import React from "react";
import { NavBar } from "../../components/NavBar";
import SideOptions from "../../components/SideOptions";
import { UserFiles } from "../../components/UserFiles";

export const UserPage: React.FC = () => {
  return (
    <>
      <NavBar />
      <div className="user-main-area">
        <UserFiles />
        <SideOptions />
      </div>
    </>
  );
};
