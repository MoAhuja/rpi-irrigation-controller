import { useEffect, useState } from 'react';
import {
  Alert,
  Box,
  Button,
  CircularProgress,
  Divider,
  FormControlLabel,
  IconButton,
  Paper,
  Stack,
  Switch,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Tooltip,
  Typography,
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import AddIcon from '@mui/icons-material/Add';
import NotificationsActiveIcon from '@mui/icons-material/NotificationsActive';
import {
  getNotificationConfig,
  setNotificationConfig,
  getPushBulletUsers,
  addPushBulletUser,
  deletePushBulletUser,
} from '../../api/client';

export default function NotificationsPanel() {
  const [config, setConfig] = useState(null);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [savingConfig, setSavingConfig] = useState(false);
  const [configSuccess, setConfigSuccess] = useState(false);
  const [error, setError] = useState(null);

  // New user form
  const [newName, setNewName] = useState('');
  const [newKey, setNewKey] = useState('');
  const [addingUser, setAddingUser] = useState(false);
  const [addError, setAddError] = useState(null);

  const loadData = () => {
    setLoading(true);
    Promise.all([getNotificationConfig(), getPushBulletUsers()])
      .then(([cfgRes, usersRes]) => {
        setConfig(cfgRes.data);
        setUsers(usersRes.data.users ?? []);
      })
      .catch(() => setError('Failed to load notification settings.'))
      .finally(() => setLoading(false));
  };

  useEffect(() => { loadData(); }, []);

  const handleConfigToggle = (field) => {
    setConfig((prev) => ({ ...prev, [field]: !prev[field] }));
  };

  const handleSaveConfig = async () => {
    setSavingConfig(true);
    setError(null);
    setConfigSuccess(false);
    try {
      await setNotificationConfig({
        notify_on_watering_start: config.notify_on_watering_start,
        notify_on_watering_stop: config.notify_on_watering_stop,
        notify_on_error: config.notify_on_error,
      });
      setConfigSuccess(true);
    } catch (err) {
      setError(err.response?.data?.message || err.message);
    } finally {
      setSavingConfig(false);
    }
  };

  const handleAddUser = async () => {
    if (!newName.trim() || !newKey.trim()) return;
    setAddingUser(true);
    setAddError(null);
    try {
      await addPushBulletUser(newName.trim(), newKey.trim());
      setNewName('');
      setNewKey('');
      loadData();
    } catch (err) {
      setAddError(err.response?.data?.message || err.message);
    } finally {
      setAddingUser(false);
    }
  };

  const handleDeleteUser = async (name) => {
    try {
      await deletePushBulletUser(name);
      loadData();
    } catch (err) {
      setError(err.response?.data?.message || err.message);
    }
  };

  return (
    <Box>
      <Typography variant="h6" fontWeight={600} gutterBottom>
        Notification Settings
      </Typography>
      <Divider sx={{ mb: 3 }} />

      {loading && <CircularProgress size={24} />}
      {error && <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>{error}</Alert>}

      {!loading && config && (
        <Stack spacing={4}>

          {/* ── Notification triggers ── */}
          <Box>
            <Typography variant="subtitle1" fontWeight={600} gutterBottom>
              Notify On
            </Typography>
            <Paper variant="outlined" sx={{ p: 2 }}>
              <Stack spacing={1}>
                <FormControlLabel
                  control={
                    <Switch
                      checked={config.notify_on_watering_start}
                      onChange={() => handleConfigToggle('notify_on_watering_start')}
                      color="success"
                    />
                  }
                  label="Watering Start"
                />
                <FormControlLabel
                  control={
                    <Switch
                      checked={config.notify_on_watering_stop}
                      onChange={() => handleConfigToggle('notify_on_watering_stop')}
                      color="success"
                    />
                  }
                  label="Watering Stop"
                />
                <FormControlLabel
                  control={
                    <Switch
                      checked={config.notify_on_error}
                      onChange={() => handleConfigToggle('notify_on_error')}
                      color="warning"
                    />
                  }
                  label="Errors"
                />
              </Stack>
            </Paper>
            {configSuccess && <Alert severity="success" sx={{ mt: 1 }}>Saved.</Alert>}
            <Button
              variant="contained"
              sx={{ mt: 2 }}
              onClick={handleSaveConfig}
              disabled={savingConfig}
            >
              {savingConfig ? 'Saving…' : 'Save Notification Triggers'}
            </Button>
          </Box>

          <Divider />

          {/* ── PushBullet Users ── */}
          <Box>
            <Box display="flex" alignItems="center" gap={1} mb={1}>
              <NotificationsActiveIcon color="action" fontSize="small" />
              <Typography variant="subtitle1" fontWeight={600}>
                PushBullet Users
              </Typography>
            </Box>
            <Typography variant="body2" color="text.secondary" mb={2}>
              Notifications are sent via PushBullet to each user in this list.
            </Typography>

            {users.length > 0 ? (
              <TableContainer component={Paper} variant="outlined" sx={{ mb: 2 }}>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell><strong>Name</strong></TableCell>
                      <TableCell><strong>API Key</strong></TableCell>
                      <TableCell padding="checkbox" />
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {users.map((user) => (
                      <TableRow key={user.name} hover>
                        <TableCell>{user.name}</TableCell>
                        <TableCell>
                          <Typography
                            variant="body2"
                            sx={{ fontFamily: 'monospace', color: 'text.secondary' }}
                          >
                            {user.api_key.slice(0, 8)}••••••••
                          </Typography>
                        </TableCell>
                        <TableCell>
                          <Tooltip title="Remove user">
                            <IconButton
                              size="small"
                              color="error"
                              onClick={() => handleDeleteUser(user.name)}
                            >
                              <DeleteIcon fontSize="small" />
                            </IconButton>
                          </Tooltip>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            ) : (
              <Alert severity="info" sx={{ mb: 2 }}>No PushBullet users configured.</Alert>
            )}

            {/* Add user form */}
            <Paper variant="outlined" sx={{ p: 2 }}>
              <Typography variant="subtitle2" gutterBottom>Add User</Typography>
              {addError && <Alert severity="error" sx={{ mb: 1 }}>{addError}</Alert>}
              <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2} alignItems="flex-start">
                <TextField
                  label="Name"
                  value={newName}
                  onChange={(e) => setNewName(e.target.value)}
                  size="small"
                  sx={{ flex: 1 }}
                />
                <TextField
                  label="PushBullet API Key"
                  value={newKey}
                  onChange={(e) => setNewKey(e.target.value)}
                  size="small"
                  sx={{ flex: 2 }}
                  type="password"
                />
                <Button
                  variant="contained"
                  startIcon={<AddIcon />}
                  onClick={handleAddUser}
                  disabled={addingUser || !newName.trim() || !newKey.trim()}
                  sx={{ whiteSpace: 'nowrap' }}
                >
                  {addingUser ? 'Adding…' : 'Add User'}
                </Button>
              </Stack>
            </Paper>
          </Box>
        </Stack>
      )}
    </Box>
  );
}
