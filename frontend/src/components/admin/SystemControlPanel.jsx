import { useEffect, useState } from 'react';
import {
  Alert,
  Box,
  Button,
  CircularProgress,
  Divider,
  FormControlLabel,
  Stack,
  Switch,
  Typography,
} from '@mui/material';
import PowerSettingsNewIcon from '@mui/icons-material/PowerSettingsNew';
import { getKillSwitch, setKillSwitch } from '../../api/client';

export default function SystemControlPanel({ onDashboardUpdate }) {
  const [killSwitch, setKillSwitchState] = useState(false);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    getKillSwitch()
      .then((res) => setKillSwitchState(res.data.kill_switch))
      .catch(() => setError('Failed to load kill switch status.'))
      .finally(() => setLoading(false));
  }, []);

  const handleToggle = async (enabled) => {
    setSaving(true);
    setError(null);
    setSuccess(false);
    try {
      await setKillSwitch(enabled);
      setKillSwitchState(enabled);
      setSuccess(true);
      if (onDashboardUpdate) onDashboardUpdate();
    } catch (err) {
      setError(err.response?.data?.message || err.message);
    } finally {
      setSaving(false);
    }
  };

  return (
    <Box>
      <Typography variant="h6" fontWeight={600} gutterBottom>
        System Control
      </Typography>
      <Divider sx={{ mb: 3 }} />

      {loading && <CircularProgress size={24} />}

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      {success && <Alert severity="success" sx={{ mb: 2 }}>Kill switch updated.</Alert>}

      {!loading && (
        <Stack spacing={3}>
          <Box
            sx={{
              p: 3,
              border: 2,
              borderRadius: 2,
              borderColor: killSwitch ? 'error.main' : 'success.main',
              bgcolor: killSwitch ? 'error.50' : 'success.50',
            }}
          >
            {/* Top row: icon + label + switch */}
            <Box display="flex" alignItems="center" justifyContent="space-between" gap={1} mb={1}>
              <Box display="flex" alignItems="center" gap={1}>
                <PowerSettingsNewIcon color={killSwitch ? 'error' : 'success'} />
                <Typography variant="subtitle1" fontWeight={600}>
                  Kill Switch
                </Typography>
              </Box>
              <FormControlLabel
                sx={{ m: 0 }}
                control={
                  <Switch
                    checked={killSwitch}
                    onChange={(e) => handleToggle(e.target.checked)}
                    color="error"
                    disabled={saving}
                  />
                }
                label={
                  <Typography fontWeight={600} color={killSwitch ? 'error.main' : 'text.secondary'}>
                    {killSwitch ? 'ON' : 'OFF'}
                  </Typography>
                }
              />
            </Box>
            <Typography variant="body2" color="text.secondary">
              When ON, all zones are prevented from running — including scheduled and manual runs.
            </Typography>
          </Box>

          <Typography variant="body2" color="text.secondary">
            Use the kill switch to immediately pause all irrigation activity without deleting your schedules.
          </Typography>
        </Stack>
      )}
    </Box>
  );
}
