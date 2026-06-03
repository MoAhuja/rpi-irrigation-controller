import { useEffect, useState } from 'react';
import {
  Box,
  Chip,
  CircularProgress,
  Collapse,
  Dialog,
  DialogContent,
  DialogTitle,
  Divider,
  Grid,
  IconButton,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import KeyboardArrowRightIcon from '@mui/icons-material/KeyboardArrowRight';
import { getZoneHistory } from '../api/client';

function fmt(isoString) {
  if (!isoString) return '—';
  return new Date(isoString).toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
    hour12: true,
  });
}

function val(v, unit = '') {
  if (v === null || v === undefined) return 'N/A';
  return `${v}${unit}`;
}

function DecisionChip({ value }) {
  const isActivate =
    value?.toLowerCase().includes('activate') &&
    !value?.toLowerCase().includes('deactivate');
  return (
    <Chip
      label={value ?? '—'}
      size="small"
      color={isActivate ? 'success' : 'default'}
      variant={isActivate ? 'filled' : 'outlined'}
    />
  );
}

function DetailField({ label, value }) {
  return (
    <Box>
      <Typography variant="caption" color="text.secondary" display="block">
        {label}
      </Typography>
      <Typography variant="body2" fontWeight={500}>
        {value}
      </Typography>
    </Box>
  );
}

function ExpandableRow({ row }) {
  const [open, setOpen] = useState(false);

  return (
    <>
      <TableRow hover sx={{ cursor: 'pointer' }} onClick={() => setOpen((o) => !o)}>
        <TableCell padding="checkbox">
          <IconButton size="small">
            {open ? (
              <KeyboardArrowDownIcon fontSize="small" />
            ) : (
              <KeyboardArrowRightIcon fontSize="small" />
            )}
          </IconButton>
        </TableCell>
        <TableCell>{fmt(row.start_time)}</TableCell>
        <TableCell>{fmt(row.end_time)}</TableCell>
        <TableCell>
          <DecisionChip value={row.decision} />
        </TableCell>
        <TableCell>
          <Typography variant="body2" color="text.secondary">
            {row.reason ?? '—'}
          </Typography>
        </TableCell>
      </TableRow>

      <TableRow>
        <TableCell colSpan={5} sx={{ py: 0, border: open ? undefined : 'none' }}>
          <Collapse in={open} timeout="auto" unmountOnExit>
            <Box sx={{ py: 2, px: 3, bgcolor: 'grey.50', borderRadius: 1, my: 1 }}>
              <Grid container spacing={2}>
                <Grid size={12}>
                  <Typography variant="subtitle2" color="primary" fontWeight={600}>
                    Rain
                  </Typography>
                </Grid>
                <Grid size={3}>
                  <DetailField label="Rain Enabled" value={val(row.rain_enabled)} />
                </Grid>
                <Grid size={3}>
                  <DetailField label="Short Term Rain Expected" value={val(row.current_3_hour_rain_forecast, ' mm')} />
                </Grid>
                <Grid size={3}>
                  <DetailField label="Short Term Rain Limit" value={val(row.rain_short_term_limit)} />
                </Grid>
                <Grid size={3}>
                  <DetailField label="Daily Rain Expected" value={val(row.current_daily_rain_forecast, ' mm')} />
                </Grid>
                <Grid size={3}>
                  <DetailField label="Daily Rain Limit" value={val(row.rain_daily_limit)} />
                </Grid>
                <Grid size={12}>
                  <Divider sx={{ my: 1 }} />
                  <Typography variant="subtitle2" color="primary" fontWeight={600}>
                    Temperature
                  </Typography>
                </Grid>
                <Grid size={3}>
                  <DetailField label="Temp Enabled" value={val(row.temperature_enabled)} />
                </Grid>
                <Grid size={3}>
                  <DetailField label="Current Temp" value={val(row.current_temp)} />
                </Grid>
                <Grid size={3}>
                  <DetailField label="Temp Lower Limit" value={val(row.temperature_lower_limit)} />
                </Grid>
                <Grid size={3}>
                  <DetailField label="Temp Upper Limit" value={val(row.temperature_upper_limit)} />
                </Grid>
              </Grid>
            </Box>
          </Collapse>
        </TableCell>
      </TableRow>
    </>
  );
}

export default function ZoneHistoryDialog({ open, zone, onClose }) {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!open || !zone) return;
    setLoading(true);
    setError(null);
    getZoneHistory(zone.id)
      .then((res) => setHistory(res.data.DecisionHistory ?? []))
      .catch(() => setError('Failed to load history.'))
      .finally(() => setLoading(false));
  }, [open, zone]);

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Stack spacing={0}>
            <Typography variant="h6" fontWeight={600}>
              Run History
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {zone?.name}
            </Typography>
          </Stack>
          <IconButton onClick={onClose} size="small">
            <CloseIcon />
          </IconButton>
        </Box>
      </DialogTitle>
      <Divider />
      <DialogContent sx={{ p: 0 }}>
        {loading && (
          <Box display="flex" justifyContent="center" py={4}>
            <CircularProgress />
          </Box>
        )}
        {error && (
          <Box p={3}>
            <Typography color="error">{error}</Typography>
          </Box>
        )}
        {!loading && !error && history.length === 0 && (
          <Box p={3}>
            <Typography color="text.secondary">No history found for this zone.</Typography>
          </Box>
        )}
        {!loading && !error && history.length > 0 && (
          <TableContainer>
            <Table size="small" stickyHeader>
              <TableHead>
                <TableRow>
                  <TableCell padding="checkbox" />
                  <TableCell><strong>Start</strong></TableCell>
                  <TableCell><strong>End</strong></TableCell>
                  <TableCell><strong>Decision</strong></TableCell>
                  <TableCell><strong>Reason</strong></TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {history.map((row, i) => (
                  <ExpandableRow key={i} row={row} />
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        )}
      </DialogContent>
    </Dialog>
  );
}
