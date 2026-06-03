import { useEffect, useState } from 'react';
import {
  Alert,
  Box,
  Button,
  CircularProgress,
  Divider,
  Stack,
  Typography,
} from '@mui/material';
import WaterDropIcon from '@mui/icons-material/WaterDrop';
import ClearIcon from '@mui/icons-material/Clear';
import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import dayjs from 'dayjs';
import { getRainDelay, setRainDelay } from '../../api/client';

export default function RainDelayPanel() {
  const [value, setValue] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    getRainDelay()
      .then((res) => {
        const raw = res.data.rain_delay;
        setValue(raw ? dayjs(raw) : null);
      })
      .catch(() => setError('Failed to load rain delay.'))
      .finally(() => setLoading(false));
  }, []);

  const handleSave = async () => {
    setSaving(true);
    setError(null);
    setSuccess(false);
    try {
      const formatted = value ? value.format('YYYY-MM-DDTHH:mm:ss') : '';
      await setRainDelay(formatted);
      setSuccess(true);
    } catch (err) {
      setError(err.response?.data?.message || err.message);
    } finally {
      setSaving(false);
    }
  };

  const handleClear = async () => {
    setSaving(true);
    setError(null);
    setSuccess(false);
    try {
      await setRainDelay('');
      setValue(null);
      setSuccess(true);
    } catch (err) {
      setError(err.response?.data?.message || err.message);
    } finally {
      setSaving(false);
    }
  };

  const isActive = value && dayjs().isBefore(value);

  return (
    <Box>
      <Typography variant="h6" fontWeight={600} gutterBottom>
        Rain Delay
      </Typography>
      <Divider sx={{ mb: 3 }} />

      {loading && <CircularProgress size={24} />}
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      {success && <Alert severity="success" sx={{ mb: 2 }}>Rain delay updated.</Alert>}

      {!loading && (
        <Stack spacing={3}>
          {isActive && (
            <Alert severity="info" icon={<WaterDropIcon />}>
              Rain delay is active until <strong>{value.format('MMM D, YYYY h:mm A')}</strong>.
              Zones will not run until then.
            </Alert>
          )}

          <Typography variant="body2" color="text.secondary">
            Set a future date and time to delay all zone runs until that point.
            Leave blank or clear to disable the rain delay.
          </Typography>

          <LocalizationProvider dateAdapter={AdapterDayjs}>
            <DateTimePicker
              label="Delay Until"
              value={value}
              onChange={(newVal) => setValue(newVal)}
              disablePast
              slotProps={{ textField: { fullWidth: true } }}
            />
          </LocalizationProvider>

          <Stack direction="row" spacing={2}>
            <Button
              variant="contained"
              onClick={handleSave}
              disabled={saving || !value}
            >
              {saving ? 'Saving…' : 'Set Rain Delay'}
            </Button>
            <Button
              variant="outlined"
              color="error"
              startIcon={<ClearIcon />}
              onClick={handleClear}
              disabled={saving || !value}
            >
              Clear Delay
            </Button>
          </Stack>
        </Stack>
      )}
    </Box>
  );
}
