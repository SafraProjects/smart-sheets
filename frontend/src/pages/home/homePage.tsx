import { useState } from "react";
import React from "react";

export const HomePage: React.FC = () => {
  const [text, setText] = useState<string>("");

  return (
    <>
      <h1>Wellcom to Home-Page</h1>
    </>
  );
};
