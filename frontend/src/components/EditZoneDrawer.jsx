import { useEffect, useState } from 'react';
import {
  Accordion,
  AccordionDetails,
  AccordionSummary,
  Alert,
  Box,
  Button,
  Checkbox,
  CircularProgress,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  Divider,
  Drawer,
  FormControl,
  FormControlLabel,
  IconButton,
  InputAdornment,
  InputLabel,
  MenuItem,
  Paper,
  Select,
  Stack,
  Switch,
  TextField,
  Typography,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import CloseIcon from '@mui/icons-material/Close';
import AddIcon from '@mui/icons-material/Add';
import DeleteIcon from '@mui/icons-material/Delete';
import { getZone, editZone, createZone, deleteZone, getRelays } from '../api/client';

const BLANK_FORM = () => ({
  zone_name: '',
  zone_description: '',
  enabled: true,
  relay: null,
  temperature: { enabled: false, min: 0, max: 40 },
  rain: { enabled: false, shortTermExpectedRainAmount: 5, dailyExpectedRainAmount: 10 },
  schedule: [],
});

const DAYS = [
  { label: 'Mon', value: 0 },
  { label: 'Tue', value: 1 },
  { label: 'Wed', value: 2 },
  { label: 'Thu', value: 3 },
  { label: 'Fri', value: 4 },
  { label: 'Sat', value: 5 },
  { label: 'Sun', value: 6 },
];

const newSchedule = () => ({
  enabled: true,
  startTime: '08:00',
  endTime: '08:30',
  schedule_type: 0,
  days: [],
});

function ScheduleCard({ sched, index, onChange, onToggleDay, onRemove }) {
  return (
    <Paper variant="outlined" sx={{ p: 2 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={1.5}>
        <FormControlLabel
          control={
            <Switch
              size="small"
              color="success"
              checked={sched.enabled}
              onChange={(e) => onChange(index, 'enabled', e.target.checked)}
            />
          }
          label={
            <Typography variant="body2" fontWeight={500}>
              Schedule {index + 1}
            </Typography>
          }
        />
        <IconButton size="small" color="error" onClick={() => onRemove(index)}>
          <DeleteIcon fontSize="small" />
        </IconButton>
      </Box>

      <Stack spacing={2}>
        <FormControl fullWidth size="small">
          <InputLabel>Type</InputLabel>
          <Select
            label="Type"
            value={sched.schedule_type}
            onChange={(e) => onChange(index, 'schedule_type', e.target.value)}
          >
            <MenuItem value={0}>Day &amp; Time</MenuItem>
            <MenuItem value={1}>Time &amp; Frequency</MenuItem>
          </Select>
        </FormControl>

        <Stack direction="row" spacing={2}>
          <TextField
            label="Start Time"
            value={sched.startTime}
            onChange={(e) => onChange(index, 'startTime', e.target.value)}
            size="small"
            placeholder="HH:MM"
            fullWidth
          />
          <TextField
            label="End Time"
            value={sched.endTime}
            onChange={(e) => onChange(index, 'endTime', e.target.value)}
            size="small"
            placeholder="HH:MM"
            fullWidth
          />
        </Stack>

        {sched.schedule_type === 0 && (
          <Box>
            <Typography variant="caption" color="text.secondary" gutterBottom display="block">
              Days of week
            </Typography>
            <Stack direction="row" spacing={0} flexWrap="wrap">
              {DAYS.map((day) => (
                <FormControlLabel
                  key={day.value}
                  label={<Typography variant="caption">{day.label}</Typography>}
                  labelPlacement="bottom"
                  sx={{ mx: 0.5 }}
                  control={
                    <Checkbox
                      size="small"
                      sx={{ p: 0.5 }}
                      checked={sched.days.includes(day.value)}
                      onChange={() => onToggleDay(index, day.value)}
                    />
                  }
                />
              ))}
            </Stack>
          </Box>
        )}
      </Stack>
    </Paper>
  );
}

export default function EditZoneDrawer({ open, zoneId, onClose, onSaved }) {
  const isCreate = !zoneId;
  const [form, setForm] = useState(null);
  const [relays, setRelays] = useState([]);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);
  const [deleteConfirmOpen, setDeleteConfirmOpen] = useState(false);
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    if (!open) return;
    setError(null);
    if (isCreate) {
      setForm(BLANK_FORM());
      getRelays().then((r) => setRelays(r.data.relays ?? [])).catch(() => {});
    } else {
      setLoading(true);
      setForm(null);
      Promise.all([getZone(zoneId), getRelays()])
        .then(([zoneRes, relayRes]) => {
          setForm(structuredClone(zoneRes.data));
          setRelays(relayRes.data.relays ?? []);
        })
        .catch(() => setError('Failed to load zone data.'))
        .finally(() => setLoading(false));
    }
  }, [open, zoneId]);

  const setField = (path, value) => {
    setForm((prev) => {
      const clone = structuredClone(prev);
      const keys = path.split('.');
      let obj = clone;
      for (let i = 0; i < keys.length - 1; i++) obj = obj[keys[i]];
      obj[keys[keys.length - 1]] = value;
      return clone;
    });
  };

  const updateSchedule = (index, key, value) => {
    setForm((prev) => {
      const clone = structuredClone(prev);
      clone.schedule[index][key] = value;
      return clone;
    });
  };

  const toggleScheduleDay = (index, day) => {
    setForm((prev) => {
      const clone = structuredClone(prev);
      const days = clone.schedule[index].days;
      clone.schedule[index].days = days.includes(day)
        ? days.filter((d) => d !== day)
        : [...days, day].sort((a, b) => a - b);
      return clone;
    });
  };

  const addSchedule = () => {
    setForm((prev) => {
      const clone = structuredClone(prev);
      clone.schedule.push(newSchedule());
      return clone;
    });
  };

  const removeSchedule = (index) => {
    setForm((prev) => {
      const clone = structuredClone(prev);
      clone.schedule.splice(index, 1);
      return clone;
    });
  };

  const handleSave = async () => {
    setSaving(true);
    setError(null);
    try {
      if (isCreate) {
        await createZone(form);
      } else {
        await editZone(form);
      }
      onSaved();
      onClose();
    } catch (err) {
      const msg = err.response?.data?.message || err.message;
      setError(`Save failed: ${msg}`);
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async () => {
    setDeleting(true);
    setError(null);
    try {
      await deleteZone(form.id);
      setDeleteConfirmOpen(false);
      onSaved();
      onClose();
    } catch (err) {
      const msg = err.response?.data?.message || err.message;
      setError(`Delete failed: ${msg}`);
      setDeleteConfirmOpen(false);
    } finally {
      setDeleting(false);
    }
  };

  return (
    <Drawer
      anchor="right"
      open={open}
      onClose={onClose}
      PaperProps={{ sx: { width: { xs: '100%', sm: 520 }, display: 'flex', flexDirection: 'column' } }}
    >
      {/* Header */}
      <Box
        sx={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          px: 3,
          py: 2,
          bgcolor: 'primary.main',
          color: 'primary.contrastText',
          flexShrink: 0,
        }}
      >
        <Box>
          <Typography variant="h6" fontWeight={700}>
            {isCreate ? 'Create Zone' : 'Edit Zone'}
          </Typography>
          {form && (
            <Typography variant="body2" sx={{ opacity: 0.85 }}>
              {form.zone_name}
            </Typography>
          )}
        </Box>
        <IconButton onClick={onClose} size="small" sx={{ color: 'inherit' }}>
          <CloseIcon />
        </IconButton>
      </Box>
      <Divider />

      {/* Scrollable body */}
      <Box sx={{ flex: 1, overflowY: 'auto', p: 2 }}>
        {loading && (
          <Box display="flex" justifyContent="center" py={6}>
            <CircularProgress />
          </Box>
        )}

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        {form && (
          <Stack spacing={1}>

            {/* ── Zone Info ── */}
            <Accordion defaultExpanded disableGutters>
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Typography fontWeight={600}>Zone Info</Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Stack spacing={2}>
                  <TextField
                    label="Name"
                    value={form.zone_name}
                    onChange={(e) => setField('zone_name', e.target.value)}
                    fullWidth
                    size="small"
                  />
                  <TextField
                    label="Description"
                    value={form.zone_description}
                    onChange={(e) => setField('zone_description', e.target.value)}
                    fullWidth
                    size="small"
                    multiline
                    rows={2}
                  />
                  <FormControlLabel
                    control={
                      <Switch
                        checked={form.enabled}
                        onChange={(e) => setField('enabled', e.target.checked)}
                        color="success"
                      />
                    }
                    label="Zone Enabled"
                  />
                </Stack>
              </AccordionDetails>
            </Accordion>

            {/* ── Schedules ── */}
            <Accordion defaultExpanded disableGutters>
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Typography fontWeight={600}>
                  Schedules ({form.schedule.length})
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Stack spacing={2}>
                  {form.schedule.map((sched, idx) => (
                    <ScheduleCard
                      key={idx}
                      sched={sched}
                      index={idx}
                      onChange={updateSchedule}
                      onToggleDay={toggleScheduleDay}
                      onRemove={removeSchedule}
                    />
                  ))}
                  <Button
                    startIcon={<AddIcon />}
                    variant="outlined"
                    size="small"
                    onClick={addSchedule}
                  >
                    Add Schedule
                  </Button>
                </Stack>
              </AccordionDetails>
            </Accordion>

            {/* ── Temperature Rule ── */}
            <Accordion disableGutters>
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Typography fontWeight={600}>Temperature Rule</Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Stack spacing={2}>
                  <FormControlLabel
                    control={
                      <Switch
                        checked={form.temperature.enabled}
                        onChange={(e) => setField('temperature.enabled', e.target.checked)}
                        color="success"
                      />
                    }
                    label="Enable temperature rule"
                  />
                  <Stack direction="row" spacing={2}>
                    <TextField
                      label="Min Temp"
                      type="number"
                      value={form.temperature.min ?? ''}
                      onChange={(e) => setField('temperature.min', Number(e.target.value))}
                      size="small"
                      fullWidth
                      disabled={!form.temperature.enabled}
                      InputProps={{
                        endAdornment: <InputAdornment position="end">°C</InputAdornment>,
                      }}
                    />
                    <TextField
                      label="Max Temp"
                      type="number"
                      value={form.temperature.max ?? ''}
                      onChange={(e) => setField('temperature.max', Number(e.target.value))}
                      size="small"
                      fullWidth
                      disabled={!form.temperature.enabled}
                      InputProps={{
                        endAdornment: <InputAdornment position="end">°C</InputAdornment>,
                      }}
                    />
                  </Stack>
                </Stack>
              </AccordionDetails>
            </Accordion>

            {/* ── Rain Rule ── */}
            <Accordion disableGutters>
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Typography fontWeight={600}>Rain Rule</Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Stack spacing={2}>
                  <FormControlLabel
                    control={
                      <Switch
                        checked={form.rain.enabled}
                        onChange={(e) => setField('rain.enabled', e.target.checked)}
                        color="success"
                      />
                    }
                    label="Enable rain rule"
                  />
                  <Stack direction="row" spacing={2}>
                    <TextField
                      label="Short Term Limit"
                      type="number"
                      value={form.rain.shortTermExpectedRainAmount ?? ''}
                      onChange={(e) =>
                        setField('rain.shortTermExpectedRainAmount', Number(e.target.value))
                      }
                      size="small"
                      fullWidth
                      disabled={!form.rain.enabled}
                      InputProps={{
                        endAdornment: <InputAdornment position="end">mm</InputAdornment>,
                      }}
                      helperText="Skip if forecast exceeds this"
                    />
                    <TextField
                      label="Daily Limit"
                      type="number"
                      value={form.rain.dailyExpectedRainAmount ?? ''}
                      onChange={(e) =>
                        setField('rain.dailyExpectedRainAmount', Number(e.target.value))
                      }
                      size="small"
                      fullWidth
                      disabled={!form.rain.enabled}
                      InputProps={{
                        endAdornment: <InputAdornment position="end">mm</InputAdornment>,
                      }}
                      helperText="Skip if daily forecast exceeds this"
                    />
                  </Stack>
                </Stack>
              </AccordionDetails>
            </Accordion>

            {/* ── Hardware ── */}
            <Accordion disableGutters>
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Typography fontWeight={600}>Hardware</Typography>
              </AccordionSummary>
              <AccordionDetails>
                <FormControl fullWidth size="small">
                  <InputLabel>Relay</InputLabel>
                  <Select
                    label="Relay"
                    value={form.relay ?? ''}
                    onChange={(e) => setField('relay', e.target.value || null)}
                  >
                    <MenuItem value="">None</MenuItem>
                    {relays.map((r) => (
                      <MenuItem key={r.relay} value={r.relay}>
                        Relay {r.relay} — Pin {r.pin}
                        {r.zone && r.zone !== form.id ? ` (Zone ${r.zone})` : ''}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </AccordionDetails>
            </Accordion>

          </Stack>
        )}
      </Box>

      {/* Footer */}
      <Divider />
      <Box sx={{ px: 3, py: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: 1, flexShrink: 0 }}>
        {!isCreate ? (
          <Button
            color="error"
            startIcon={<DeleteIcon />}
            onClick={() => setDeleteConfirmOpen(true)}
            disabled={saving || loading || !form}
          >
            Delete Zone
          </Button>
        ) : <Box />}
        <Box display="flex" gap={1}>
          <Button onClick={onClose} disabled={saving}>
            Cancel
          </Button>
          <Button
            variant="contained"
            onClick={handleSave}
            disabled={saving || loading || !form}
          >
            {saving ? (isCreate ? 'Creating…' : 'Saving…') : (isCreate ? 'Create Zone' : 'Save Changes')}
          </Button>
        </Box>
      </Box>

      {/* Delete confirmation dialog */}
      <Dialog open={deleteConfirmOpen} onClose={() => setDeleteConfirmOpen(false)}>
        <DialogTitle>Delete zone?</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Permanently delete <strong>{form?.zone_name}</strong>? This cannot be undone.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteConfirmOpen(false)} disabled={deleting}>Cancel</Button>
          <Button color="error" variant="contained" onClick={handleDelete} disabled={deleting}>
            {deleting ? 'Deleting…' : 'Delete'}
          </Button>
        </DialogActions>
      </Dialog>
    </Drawer>
  );
}
