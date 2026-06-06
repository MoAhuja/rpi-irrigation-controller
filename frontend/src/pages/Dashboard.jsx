import { useCallback, useEffect, useState } from 'react';
import {
  Alert,
  Box,
  Button,
  CircularProgress,
  Divider,
  Grid,
  IconButton,
  Paper,
  Snackbar,
  Tooltip,
  Typography,
} from '@mui/material';
import RefreshIcon from '@mui/icons-material/Refresh';
import AddIcon from '@mui/icons-material/Add';
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

  // Create drawer state
  const [createDrawer, setCreateDrawer] = useState(false);

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
    <Box sx={{ p: { xs: 2, md: 4 }, maxWidth: 900, mx: 'auto' }}>
      {/* System summary bar */}
      <Paper elevation={2} sx={{ p: 2, mb: 3, borderRadius: 2, background: 'linear-gradient(135deg, #e8f5e9 0%, #e3f2fd 100%)', borderTop: 4, borderColor: 'primary.main' }}>
        <Box display="flex" justifyContent="space-between" alignItems="flex-start" gap={1}>
          <Grid container spacing={1.5} sx={{ flex: 1 }}>
            {/* Location */}
            <Grid size={{ xs: 6, sm: 3 }}>
              <Box display="flex" alignItems="center" gap={1}>
                <LocationOnIcon fontSize="small" color="primary" />
                <Box>
                  <Typography variant="caption" color="text.secondary" display="block">Location</Typography>
                  <Typography variant="body2" fontWeight={600}>
                    {systemSettings ? `${systemSettings.city}, ${systemSettings.country}` : '—'}
                  </Typography>
                </Box>
              </Box>
            </Grid>

            {/* Kill Switch */}
            <Grid size={{ xs: 6, sm: 3 }}>
              <Box display="flex" alignItems="center" gap={1}>
                <PauseCircleIcon fontSize="small" color={systemSettings?.kill_switch ? 'error' : 'action'} />
                <Box>
                  <Typography variant="caption" color="text.secondary" display="block">Kill Switch</Typography>
                  <FormControlLabel
                    sx={{ m: 0 }}
                    control={
                      <Switch
                        size="small"
                        color="error"
                        checked={systemSettings?.kill_switch ?? false}
                        onChange={(e) => handleKillSwitchToggle(e.target.checked)}
                        sx={{ mr: 0.5 }}
                      />
                    }
                    label={
                      <Typography variant="body2" fontWeight={600} color={systemSettings?.kill_switch ? 'error.main' : 'text.primary'}>
                        {systemSettings?.kill_switch ? 'ON' : 'OFF'}
                      </Typography>
                    }
                  />
                </Box>
              </Box>
            </Grid>

            {/* Rain Delay */}
            <Grid size={{ xs: 6, sm: 3 }}>
              <Box display="flex" alignItems="center" gap={1}>
                <WaterDropIcon fontSize="small" color={systemSettings?.rain_delay ? 'info' : 'action'} />
                <Box>
                  <Typography variant="caption" color="text.secondary" display="block">Rain Delay</Typography>
                  <Typography variant="body2" fontWeight={600} color={systemSettings?.rain_delay ? 'info.main' : 'text.primary'}>
                    {systemSettings?.rain_delay ? formatDateTime(systemSettings.rain_delay) : 'OFF'}
                  </Typography>
                </Box>
              </Box>
            </Grid>

            {/* Engine Last Ran */}
            <Grid size={{ xs: 6, sm: 3 }}>
              <Box display="flex" alignItems="center" gap={1}>
                <ScheduleIcon fontSize="small" color="action" />
                <Box>
                  <Typography variant="caption" color="text.secondary" display="block">Engine Last Ran</Typography>
                  <Typography variant="body2" fontWeight={600}>
                    {systemSettings ? formatDateTime(systemSettings.engine_last_ran) : '—'}
                  </Typography>
                </Box>
              </Box>
            </Grid>
          </Grid>

          <Tooltip title="Refresh">
            <IconButton onClick={fetchDashboard} disabled={loading} size="small">
              <RefreshIcon />
            </IconButton>
          </Tooltip>
        </Box>
      </Paper>

      {/* Zones header */}
      <Box display="flex" alignItems="center" justifyContent="space-between" mb={2} mt={1}>
        <Typography variant="h6" fontWeight={600}>
          Zones
        </Typography>
        <Typography variant="body2" color="text.secondary">
          {dashboardData?.zones?.filter((z) => z.is_running).length ?? 0} running
        </Typography>
      </Box>
      <Divider sx={{ mb: 2 }} />

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
        <Grid container spacing={2.5}>
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

      {/* Create Zone button */}
      <Divider sx={{ mt: 5, mb: 4 }} />
      <Box display="flex" justifyContent="center" pb={4}>
        <Button
          variant="contained"
          size="large"
          startIcon={<AddIcon />}
          onClick={() => setCreateDrawer(true)}
          sx={{
            borderRadius: 8,
            px: 6,
            py: 1.5,
            fontSize: '1rem',
            boxShadow: 6,
            '&:hover': { boxShadow: 12, transform: 'translateY(-2px)' },
            transition: 'box-shadow 0.2s, transform 0.2s',
          }}
        >
          Create Zone
        </Button>
      </Box>

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

      {/* Create drawer */}
      <EditZoneDrawer
        open={createDrawer}
        zoneId={null}
        onClose={() => setCreateDrawer(false)}
        onSaved={() => {
          showToast('Zone created successfully', 'success');
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
