import { useEffect, useState } from 'react';
import {
  Alert,
  Box,
  Button,
  CircularProgress,
  Divider,
  Stack,
  TextField,
  Typography,
} from '@mui/material';
import { getLocation, setLocation } from '../../api/client';

export default function WeatherPanel() {
  const [city, setCity] = useState('');
  const [country, setCountry] = useState('');
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    getLocation()
      .then((res) => {
        setCity(res.data.city ?? '');
        setCountry(res.data.country ?? '');
      })
      .catch(() => setError('Failed to load weather settings.'))
      .finally(() => setLoading(false));
  }, []);

  const handleSave = async () => {
    setSaving(true);
    setError(null);
    setSuccess(false);
    try {
      await setLocation(city, country);
      setSuccess(true);
    } catch (err) {
      setError(err.response?.data?.message || err.message);
    } finally {
      setSaving(false);
    }
  };

  return (
    <Box>
      <Typography variant="h6" fontWeight={600} gutterBottom>
        Weather Settings
      </Typography>
      <Divider sx={{ mb: 3 }} />

      {loading && <CircularProgress size={24} />}
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      {success && <Alert severity="success" sx={{ mb: 2 }}>Weather settings saved.</Alert>}

      {!loading && (
        <Stack spacing={3}>
          <Typography variant="body2" color="text.secondary">
            The city and country are used to fetch weather forecasts from OpenWeatherMap,
            which determine whether scheduled zones should run based on rain and temperature rules.
          </Typography>

          <Stack direction="row" spacing={2}>
            <TextField
              label="City"
              value={city}
              onChange={(e) => setCity(e.target.value)}
              fullWidth
              size="small"
              placeholder="e.g. Mississauga"
            />
            <TextField
              label="Country Code"
              value={country}
              onChange={(e) => setCountry(e.target.value.toUpperCase())}
              size="small"
              sx={{ width: 140 }}
              placeholder="e.g. CA"
              inputProps={{ maxLength: 2 }}
              helperText="ISO 3166-1 alpha-2"
            />
          </Stack>

          <Alert severity="info" sx={{ fontSize: '0.8rem' }}>
            The OpenWeatherMap API key is configured in the backend source code
            (<code>service/weather_hub/weather_center.py</code>). To change it,
            update it there and restart the service.
          </Alert>

          <Box>
            <Button variant="contained" onClick={handleSave} disabled={saving || !city || !country}>
              {saving ? 'Saving…' : 'Save'}
            </Button>
          </Box>
        </Stack>
      )}
    </Box>
  );
}
