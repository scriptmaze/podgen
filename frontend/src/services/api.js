import axios from "axios";

const API = axios.create({
  baseURL: "https://podgen-qdyx.onrender.com/", // Backend URL
});

export default API;
