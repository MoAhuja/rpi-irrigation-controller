import { useCallback, useEffect, useState } from 'react';
import {
  Alert,
  Box,
  CircularProgress,
  Divider,
  Grid,
  IconButton,
  Paper,
  Snackbar,
  Stack,
  Tooltip,
  Typography,
} from '@mui/material';
import RefreshIcon from '@mui/icons-material/Refresh';
import WaterDropIcon from '@mui/icons-material/WaterDrop';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import PauseCircleIcon from '@mui/icons-material/PauseCircle';
import ScheduleIcon from '@mui/icons-material/Schedule';
import { Switch, FormControlLabel } from '@mui/material';

import { getDashboard, activateZone, deactivateZone, setKillSwitch } from '../api/client';
import ZoneCard from '../components/ZoneCard';
import StartZoneDialog from '../components/StartZoneDialog';
import ZoneHistoryDialog from '../components/ZoneHistoryDialog';
import EditZoneDrawer from '../components/EditZoneDrawer';

function formatDateTime(isoString) {
  if (!isoString) return 'N/A';
  return new Date(isoString).toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
    hour12: true,
  });
}

export default function Dashboard({ refreshKey }) {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Start dialog state
  const [startDialog, setStartDialog] = useState({ open: false, zone: null });

  // History dialog state
  const [historyDialog, setHistoryDialog] = useState({ open: false, zone: null });

  // Edit drawer state
  const [editDrawer, setEditDrawer] = useState({ open: false, zoneId: null });

  // Toast notifications
  const [toast, setToast] = useState({ open: false, message: '', severity: 'success' });

  const fetchDashboard = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await getDashboard();
      setDashboardData(res.data);
    } catch (err) {
      setError('Failed to load dashboard. Check that the backend is reachable.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchDashboard();
    // Auto-refresh every 30 seconds
    const interval = setInterval(fetchDashboard, 30000);
    return () => clearInterval(interval);
  }, [fetchDashboard, refreshKey]);

  const handleKillSwitchToggle = async (enabled) => {
    try {
      await setKillSwitch(enabled);
      fetchDashboard();
    } catch (err) {
      showToast('Failed to update kill switch', 'error');
    }
  };

  const handleStartClick = (zone) => {
    setStartDialog({ open: true, zone });
  };

  const handleStartConfirm = async (duration) => {
    const { zone } = startDialog;
    setStartDialog({ open: false, zone: null });
    try {
      await activateZone(zone.id, duration);
      showToast(`Started "${zone.name}" for ${duration} min`, 'success');
      fetchDashboard();
    } catch (err) {
      const msg = err.response?.data?.message || err.message;
      showToast(`Failed to start zone: ${msg}`, 'error');
    }
  };

  const handleStop = async (zoneId) => {
    const zone = dashboardData.zones.find((z) => z.id === zoneId);
    try {
      await deactivateZone(zoneId);
      showToast(`Stopped "${zone?.name}"`, 'success');
      fetchDashboard();
    } catch (err) {
      const msg = err.response?.data?.message || err.message;
      showToast(`Failed to stop zone: ${msg}`, 'error');
    }
  };

  const handleEdit = (zoneId) => {
    setEditDrawer({ open: true, zoneId });
  };

  const handleHistory = (zone) => {
    setHistoryDialog({ open: true, zone });
  };

  const showToast = (message, severity = 'success') => {
    setToast({ open: true, message, severity });
  };

  const systemSettings = dashboardData?.system_settings;

  return (
    <Box sx={{ p: { xs: 2, md: 3 } }}>
      {/* System summary bar */}
      <Paper elevation={1} sx={{ p: 2, mb: 3, borderRadius: 2 }}>
        <Box display="flex" justifyContent="space-between" alignItems="center" flexWrap="wrap" gap={2}>
          <Stack direction="row" spacing={3} flexWrap="wrap">
            <Box display="flex" alignItems="center" gap={0.5}>
              <LocationOnIcon fontSize="small" color="action" />
              <Typography variant="body2">
                <strong>Location:</strong>{' '}
                {systemSettings ? `${systemSettings.city}, ${systemSettings.country}` : '—'}
              </Typography>
            </Box>
            <Box display="flex" alignItems="center" gap={0.5}>
              <PauseCircleIcon
                fontSize="small"
                color={systemSettings?.kill_switch ? 'error' : 'action'}
              />
              <FormControlLabel
                sx={{ m: 0 }}
                control={
                  <Switch
                    size="small"
                    color="error"
                    checked={systemSettings?.kill_switch ?? false}
                    onChange={(e) => handleKillSwitchToggle(e.target.checked)}
                    sx={{ mx: 0.5 }}
                  />
                }
                label={
                  <Typography variant="body2">
                    <strong>Kill Switch:</strong>{' '}
                    {systemSettings?.kill_switch ? 'ON' : 'OFF'}
                  </Typography>
                }
              />
            </Box>
            <Box display="flex" alignItems="center" gap={0.5}>
              <WaterDropIcon fontSize="small" color="action" />
              <Typography variant="body2">
                <strong>Rain Delay:</strong>{' '}
                {systemSettings?.rain_delay
                  ? formatDateTime(systemSettings.rain_delay)
                  : 'OFF'}
              </Typography>
            </Box>
            <Box display="flex" alignItems="center" gap={0.5}>
              <ScheduleIcon fontSize="small" color="action" />
              <Typography variant="body2">
                <strong>Engine Last Ran:</strong>{' '}
                {systemSettings ? formatDateTime(systemSettings.engine_last_ran) : '—'}
              </Typography>
            </Box>
          </Stack>

          <Tooltip title="Refresh">
            <IconButton onClick={fetchDashboard} disabled={loading}>
              <RefreshIcon />
            </IconButton>
          </Tooltip>
        </Box>
      </Paper>

      {/* Zones header */}
      <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
        <Typography variant="h6" fontWeight={600}>
          Zones
        </Typography>
        <Typography variant="body2" color="text.secondary">
          {dashboardData?.zones?.filter((z) => z.is_running).length ?? 0} running
        </Typography>
      </Box>
      <Divider sx={{ mb: 3 }} />

      {/* Loading / Error / Zones grid */}
      {loading && !dashboardData && (
        <Box display="flex" justifyContent="center" mt={6}>
          <CircularProgress />
        </Box>
      )}

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {dashboardData && (
        <Grid container spacing={2}>
          {dashboardData.zones.map((zone) => (
            <Grid size={12} key={zone.id}>
              <ZoneCard
                zone={zone}
                onStart={handleStartClick}
                onStop={handleStop}
                onEdit={handleEdit}
                onHistory={handleHistory}
              />
            </Grid>
          ))}
        </Grid>
      )}

      {/* Start duration dialog */}
      <StartZoneDialog
        open={startDialog.open}
        zoneName={startDialog.zone?.name ?? ''}
        onConfirm={handleStartConfirm}
        onCancel={() => setStartDialog({ open: false, zone: null })}
      />

      {/* History dialog */}
      <ZoneHistoryDialog
        open={historyDialog.open}
        zone={historyDialog.zone}
        onClose={() => setHistoryDialog({ open: false, zone: null })}
      />

      {/* Edit drawer */}
      <EditZoneDrawer
        open={editDrawer.open}
        zoneId={editDrawer.zoneId}
        onClose={() => setEditDrawer({ open: false, zoneId: null })}
        onSaved={() => {
          showToast('Zone saved successfully', 'success');
          fetchDashboard();
        }}
      />

      {/* Toast */}
      <Snackbar
        open={toast.open}
        autoHideDuration={4000}
        onClose={() => setToast((t) => ({ ...t, open: false }))}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert
          severity={toast.severity}
          onClose={() => setToast((t) => ({ ...t, open: false }))}
          variant="filled"
        >
          {toast.message}
        </Alert>
      </Snackbar>
    </Box>
  );
}
