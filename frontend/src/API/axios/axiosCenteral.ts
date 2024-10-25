import { UserDBDto, UserLogin, UserSignInDto } from "../../../interface/user.dtos";
import { genericPost, genericGet, genericDelete, genericPatch } from "./axiosCenteralBase";

export const singUp = async (user_data: UserSignInDto): Promise<{ message: string }> => {
  const url = "/auto/sign-in";
  return await genericPost(user_data, url);
};

export const verifyEmail = async (temp_token: string): Promise<{ message: string }> => {
  const url = "/auto/verify-email/" + temp_token;
  return await genericPost({}, url);
};

export const login = async (user_data: UserLogin): Promise<UserDBDto> => {
  const url = "/auto/log-in";
  return await genericPost(user_data, url);
};

// export const login = async (user_data: UserLogin): Promise<UserDBDto> => {
//   const url = "/auto/log-in";
//   const user = (await genericPost(user_data, url)) as {
//     _id: string;
//     name: string;
//     email: string;
//     user_type: "user" | "admin" | "super_admin";
//   }; // מיפוי הסוגים

//   return {
//     id: user._id,
//     name: user.name,
//     email: user.email,
//     user_type: user.user_type,
//   };
// };

export const resendVerificationEmail = async (email: string): Promise<{ message: string }> => {
  const url = "/auto/resend-verification-email/" + email;
  return await genericPost({}, url);
};

export const sendPasswordToUser = async (email: string): Promise<{ message: string }> => {
  const url = "/auto/send-verification-password/" + email;
  return await genericPost({}, url);
};

export const verifyPassword = async (user_data: UserLogin): Promise<{ message: string }> => {
  const url = `/auto/verify-password/${user_data.email}/${user_data.password}`;
  return await genericPost({}, url);
};

export const recreatePassword = async (user_data: UserLogin): Promise<{ message: string }> => {
  const url = `/auto/update-password/${user_data.email}/${user_data.password}`;
  return await genericPost({}, url);
};
