import React, { useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { verify_email } from "../../../API/axios/axiosCenteral";

export const Verify = () => {
  const param = useParams<Record<string, string | undefined>>();
  const nav = useNavigate();

  const isWatieTrue = param.value === "waite";
  const isCreateingCode = param.value === "create-code";

  useEffect(() => {
    const a = async () => {
      const token = param.value;
      if (token !== "") {
        const response = await verify_email(token as string);
        if (response) {
          nav("/auto/verify/waite");
          console.log(response.message);
        }
      }
    };
    a();
  }, [!isWatieTrue && !isCreateingCode]);

  return (
    <div className="log-back">
      {isWatieTrue ? <div>verifyEmail</div> : <div>not fund</div>}
    </div>
  );
};
