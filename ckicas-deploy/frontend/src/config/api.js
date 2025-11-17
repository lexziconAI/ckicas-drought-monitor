// API Configuration for CKICAS Dashboard
// For Option B (Single Service): Use relative URLs since frontend and backend are on the same domain

const API_BASE_URL = import.meta.env.VITE_API_URL || '';  // Empty string = relative URLs

export const API_CONFIG = {
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
};

export default API_BASE_URL;