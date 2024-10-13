import React, { useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { verify_email } from "../../../API/axios/axiosCenteral";

export const VerifyEmail = () => {
  const param = useParams<Record<string, string | undefined>>();
  const nav = useNavigate();

  const isWatieTrue = param.value === "wait";
  const token = param.value;

  useEffect(() => {
    const a = async () => {
      const response = await verify_email(token as string);
      if (response) {
        nav("/auto/verify-email/wait");
        console.log(response.message);
      }
    };
    a();
  }, [token !== "wait"]);

  return (
    <div className="log-back">
      {isWatieTrue ? <div>verifyEmail</div> : <div>not fund</div>}
    </div>
  );
};
