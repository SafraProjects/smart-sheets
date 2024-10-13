import axios, { AxiosError, AxiosResponse } from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
});

// List of URLs that require authentication
const authRequiredUrls = ["/user", "/admin", "/super_admin"];

api.interceptors.response.use(
  (response: AxiosResponse) => response,
  async (error: AxiosError) => {
    const requestUrl = error.config?.url || "";

    // Check if the request URL is in the list of URLs that require authentication
    const requiresAuth = authRequiredUrls.some((authUrl) => requestUrl.includes(authUrl));

    if (error.response && error.response.status === 401 && requiresAuth) {
      // Only attempt to refresh the token if the URL requires authentication
      if (error.config) {
        try {
          // Perform token refresh request
          const refreshResponse = await api.post("/refresh-token", null);
          const newEnvToken = refreshResponse.data.access_token;

          // Update the access token in cookies
          document.cookie = `access_token=${newEnvToken}; httponly; secure;`;

          // Update the access token in the headers of the original request
          error.config.headers["Authorization"] = `Bearer ${newEnvToken}`;

          // Resend the original request with the new token
          return api.request(error.config);
        } catch (refreshError) {
          console.error("Failed to refresh token:", refreshError);
          return Promise.reject(refreshError);
        }
      }
    }

    // Handle specific HTTP errors
    if (error.response) {
      switch (error.response.status) {
        case 400:
          return Promise.reject(new Error("Bad Request"));
        case 401:
          return Promise.reject(new Error("Unauthorized"));
        case 404:
          return Promise.reject(new Error("Not Found"));
        case 409:
          return Promise.reject(new Error("Email field must be unique"));
        case 500:
          return Promise.reject(new Error("Internal Server Error"));
      }
    }

    // Handle network errors
    if (error.request) {
      return Promise.reject(new Error("Network Error"));
    }

    // Handle other errors
    return Promise.reject(new Error(`An error occurred: ${error.message}`));
  }
);

// Generic Get function
export const genericGet = async <RequestDTO extends object, ResponseDTO extends object>(
  requestDTO: RequestDTO,
  url: string
): Promise<ResponseDTO> => {
  try {
    const response: AxiosResponse<ResponseDTO> = await api.get<ResponseDTO>(url, {
      params: requestDTO,
    });
    console.log("response.data: ", response.data);
    return response.data as ResponseDTO;
  } catch (error) {
    console.log("<<< error: ", error);
    throw new Error(`General error: ${error}`);
  }
};

export const genericPost = async <RequestDTO extends object, ResponseDTO extends object>(
  requestDTO: RequestDTO,
  url: string
): Promise<ResponseDTO> => {
  try {
    console.log(requestDTO);
    const response: AxiosResponse<ResponseDTO> = await api.post<ResponseDTO>(url, requestDTO);
    console.log("response.data: ", response.data);
    return response.data as ResponseDTO;
  } catch (error) {
    console.log("<<< error: ", error);

    throw new Error(`General error: ${error}`);
  }
};

export const genericPatch = async <RequestDTO extends object, ResponseDTO extends object>(
  requestDTO: RequestDTO,
  url: string
): Promise<ResponseDTO> => {
  try {
    const response: AxiosResponse<ResponseDTO> = await api.patch<ResponseDTO>(url, requestDTO);
    console.log("response.data: ", response.data);
    return response.data as ResponseDTO;
  } catch (error) {
    console.log("<<< error: ", error);
    throw new Error(`General error: ${error}`);
  }
};

// Generic Put function
export const genericDelete = async <RequestDTO extends object, ResponseDTO extends object>(
  requestDTO: RequestDTO,
  url: string
): Promise<ResponseDTO> => {
  try {
    const response: AxiosResponse<ResponseDTO> = await api.delete<ResponseDTO>(url, requestDTO);
    return response.data as ResponseDTO;
  } catch (error) {
    console.error(error);
    throw new Error(`General error: ${error}`);
  }
};
