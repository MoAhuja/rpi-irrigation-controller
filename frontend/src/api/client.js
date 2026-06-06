import axios from 'axios';

// In development, auth is injected by the Vite proxy.
// In production, credentials are baked in at build time from .env
const authHeader = import.meta.env.VITE_API_USERNAME
  ? 'Basic ' + btoa(`${import.meta.env.VITE_API_USERNAME}:${import.meta.env.VITE_API_PASSWORD}`)
  : undefined;

const client = axios.create({
  baseURL: '',
  headers: {
    'Content-Type': 'application/json',
    ...(authHeader ? { Authorization: authHeader } : {}),
  },
});

export const getDashboard = () => client.get('/service_hub/dashboard');

export const getZone = (id) => client.get(`/service_hub/zone/${id}`);
export const editZone = (data) => client.post('/service_hub/zone/edit', data);
export const createZone = (data) => client.post('/service_hub/zone', data);
export const deleteZone = (id) => client.delete(`/service_hub/zone/${id}`);

export const activateZone = (id, duration) =>
  client.post('/service_hub/zones/activate', { id, duration });
export const deactivateZone = (id) =>
  client.post('/service_hub/zones/deactivate', { id });

export const getZoneHistory = (zoneId) =>
  client.get(`/service_hub/decisionhistory?zone=${zoneId}`);

// Relays
export const getRelays = () => client.get('/service_hub/relays');
export const addRelay = (relay, pin) => client.post('/service_hub/relay', { relay, pin });
export const deleteRelay = (relayId) => client.delete(`/service_hub/relays/${relayId}`);

// Settings — Kill Switch
export const getKillSwitch = () => client.get('/service_hub/settings/kill');
export const setKillSwitch = (enabled) =>
  client.post('/service_hub/settings/kill', { value: enabled });

// Settings — Rain Delay
export const getRainDelay = () => client.get('/service_hub/settings/raindelay');
export const setRainDelay = (value) =>
  client.post('/service_hub/settings/raindelay', { value });

// Settings — Location / Weather
export const getLocation = () => client.get('/service_hub/settings/location');
export const setLocation = (city, country) =>
  client.post('/service_hub/settings/location', { city, country });

// Settings — Notifications
export const getNotificationConfig = () =>
  client.get('/service_hub/settings/notification/config');
export const setNotificationConfig = (config) =>
  client.post('/service_hub/settings/notification/config', config);
export const getPushBulletUsers = () =>
  client.get('/service_hub/settings/notification/pushbullet/users');
export const addPushBulletUser = (name, api_key) =>
  client.post('/service_hub/settings/notification/pushbullet/user', { name, api_key });
export const deletePushBulletUser = (name) =>
  client.delete(`/service_hub/settings/notification/pushbullet/user/${name}`);

export default client;

