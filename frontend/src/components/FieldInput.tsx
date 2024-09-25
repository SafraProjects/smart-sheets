import React, { useState } from "react";

const TableFieldInput: React.FC = () => {
  const [inputValue, setInputValue] = useState<string>("");

  const handleChange = (input: string) => {
    setInputValue(input);
  };

  return (
    <div className="table-input-area">
      <input
        className="table-input"
        type="text"
        value={inputValue}
        onChange={(e) => handleChange(e.target.value)}
        placeholder="הכנס טקסט"
      />
    </div>
  );
};

export default TableFieldInput;
