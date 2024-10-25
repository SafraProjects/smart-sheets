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

    // Handle specific HTTP errors with more cases
    if (error.response) {
      console.error("Error details:", {
        status: error.response.status,
        data: error.response.data,
        headers: error.response.headers,
      });

      switch (error.response.status) {
        case 400:
          return Promise.reject(new Error(`Bad Request: ${JSON.stringify(error.response.data)}`));
        case 401:
          return Promise.reject(new Error(`Unauthorized: ${JSON.stringify(error.response.data)}`));
        case 403:
          return Promise.reject(new Error(`Forbidden: You don't have permission to access this resource.`));
        case 404:
          return Promise.reject(new Error(`Not Found: ${JSON.stringify(error.response.data)}`));
        case 408:
          return Promise.reject(new Error(`Request Timeout: The server took too long to respond.`));
        case 409:
          const conflictData = error.response?.data;
          const conflictMessage =
            conflictData && typeof conflictData === "object" && "message" in conflictData
              ? (conflictData as { message: string }).message
              : "Conflict: Email field must be unique";

          return Promise.reject(new Error(`Conflict: ${conflictMessage}`));
        case 413:
          return Promise.reject(new Error(`Payload Too Large: The request entity is too large to be processed.`));
        case 429:
          return Promise.reject(
            new Error(`Too Many Requests: You have sent too many requests in a given amount of time.`)
          );
        case 500:
          return Promise.reject(new Error(`Internal Server Error: ${JSON.stringify(error.response.data)}`));
        case 502:
          return Promise.reject(
            new Error(`Bad Gateway: The server received an invalid response from the upstream server.`)
          );
        case 503:
          return Promise.reject(
            new Error(
              `Service Unavailable: The server is currently unable to handle the request due to a temporary overload or maintenance.`
            )
          );
        case 504:
          return Promise.reject(
            new Error(`Gateway Timeout: The server didn't receive a timely response from the upstream server.`)
          );
        default:
          return Promise.reject(
            new Error(`Unexpected error: ${error.response.status}, ${JSON.stringify(error.response.data)}`)
          );
      }
    }

    // Handle network errors
    if (error.request) {
      console.error("Network error:", error.request);
      return Promise.reject(new Error("Network Error - Please check your internet connection."));
    }

    // Handle other errors (e.g., config errors)
    console.error("Error message:", error.message);
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
    console.error("Error during GET request:", error);
    throw error; // Pass the full error object
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
    console.error("Error during POST request:", error);
    throw error; // Pass the full error object
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
    console.error("Error during PATCH request:", error);
    throw error; // Pass the full error object
  }
};

// Generic Delete function
export const genericDelete = async <RequestDTO extends object, ResponseDTO extends object>(
  requestDTO: RequestDTO,
  url: string
): Promise<ResponseDTO> => {
  try {
    const response: AxiosResponse<ResponseDTO> = await api.delete<ResponseDTO>(url, { data: requestDTO });
    return response.data as ResponseDTO;
  } catch (error) {
    console.error("Error during DELETE request:", error);
    throw error; // Pass the full error object
  }
};
