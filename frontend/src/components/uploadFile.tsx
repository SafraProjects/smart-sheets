import React, { useState } from "react";

const FileUpload: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [error, setError] = useState<string>("");

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0]; // בחר את הקובץ הראשון שנבחר
    if (selectedFile) {
      const validExtensions = [".xls", ".xlsx", ".csv"];
      const fileExtension = selectedFile.name.split(".").pop();

      if (validExtensions.includes(`.${fileExtension}`)) {
        setFile(selectedFile);
        setError("");
      } else {
        setError("אנא העלה קובץ מסוג Excel (.xls, .xlsx) או CSV (.csv)");
        setFile(null);
      }
    }
  };

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (file) {
      // עשה משהו עם הקובץ (למשל, שלח אותו לשרת)
      console.log("הקובץ נבחר:", file.name);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="file"
        accept=".xls,.xlsx,.csv"
        multiple
        onChange={handleFileChange}
        placeholder="."
      />
      {error && <p style={{ color: "red" }}>{error}</p>}
      <button type="submit" disabled={!file}>
        העלה קובץ
      </button>
    </form>
  );
};

export default FileUpload;
