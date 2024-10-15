import { UserDBDto, UserLogin, UserSignInDto } from "../../../interface/user.dtos";
import { genericPost, genericGet, genericDelete, genericPatch } from "./axiosCenteralBase";

export const singUp = async (user_data: UserSignInDto): Promise<{ message: string }> => {
  const url = "/auto/sign-in";
  return await genericPost(user_data, url);
};

export const verify_email = async (temp_token: string): Promise<{ message: string }> => {
  const url = "/auto/verify-email/" + temp_token;
  return await genericPost({}, url);
};

export const login = async (user_data: UserLogin): Promise<UserDBDto> => {
  const url = "/auto/log-in";
  return await genericPost(user_data, url);
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
