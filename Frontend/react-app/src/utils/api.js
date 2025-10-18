import axios from "axios";

export const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "";

export const postVerify = (claim) =>
  axios.post(`${API_BASE_URL}/api/verify`, { claim });

const client = axios.create({
  baseURL: API_BASE_URL || undefined,
});

export default client;
