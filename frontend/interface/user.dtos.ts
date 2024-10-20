import { IsEmail, IsNotEmpty, IsString, Matches } from "class-validator";

export class UserLogin {
  @IsNotEmpty({ message: "Email is required" })
  @IsEmail()
  email: string;

  @IsNotEmpty({ message: "Password is required" })
  @IsString()
  password: string;
}

export class UserSignInDto {
  @IsNotEmpty({ message: "name is required" })
  @IsString()
  name: string;

  @IsNotEmpty({ message: "Email is required" })
  @IsEmail({}, { message: "Invalid email address" })
  email: string;

  @IsNotEmpty({ message: "Password is required" })
  @IsString()
  password: string;

  @IsNotEmpty({ message: "Phone number is required" })
  @Matches(/^\+?[1-9]\d{1,14}$/, { message: "Invalid phone number" })
  phoneNumber?: string;
}

export class UserDBDto {
  @IsNotEmpty({ message: "Id is required" })
  @IsString()
  id: string;

  @IsNotEmpty({ message: "name is required" })
  @IsString()
  name: string;

  @IsNotEmpty({ message: "Email is required" })
  @IsEmail({}, { message: "Invalid email address" })
  email: string;

  @IsNotEmpty({ message: "User Type is required" })
  @IsString()
  user_type: "user" | "admin" | "super_admin";
}
