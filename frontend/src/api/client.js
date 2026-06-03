import axios from 'axios';

// Auth is handled by the Vite proxy in development.
// In production, configure a reverse proxy with Basic Auth on the server.
const client = axios.create({
  baseURL: '',
  headers: { 'Content-Type': 'application/json' },
});

export const getDashboard = () => client.get('/service_hub/dashboard');

export const getZone = (id) => client.get(`/service_hub/zone/${id}`);

export const editZone = (data) => client.post('/service_hub/zone/edit', data);

export const activateZone = (id, duration) =>
  client.post('/service_hub/zones/activate', { id, duration });

export const deactivateZone = (id) =>
  client.post('/service_hub/zones/deactivate', { id });

export const getZoneHistory = (zoneId) =>
  client.get(`/service_hub/decisionhistory?zone=${zoneId}`);

export const getRelays = () => client.get('/service_hub/relays');

export default client;
