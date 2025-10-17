import axios from "axios";

const API_BASE = process.env.REACT_APP_API_BASE || "";

export const postVerify = (claim) => {
  return axios.post(`${API_BASE}/api/verify`, { claim });
};

const client = axios.create({
  baseURL: API_BASE,
});

export default client;
