import { useEffect, useState } from 'react';
import {
  Alert,
  Box,
  Button,
  CircularProgress,
  Divider,
  IconButton,
  Paper,
  Stack,
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
import { getRelays, addRelay, deleteRelay } from '../../api/client';

export default function RelayMapPanel() {
  const [relays, setRelays] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [newRelay, setNewRelay] = useState('');
  const [newPin, setNewPin] = useState('');
  const [adding, setAdding] = useState(false);
  const [addError, setAddError] = useState(null);

  const loadRelays = () => {
    setLoading(true);
    getRelays()
      .then((res) => setRelays(res.data.relays ?? []))
      .catch(() => setError('Failed to load relay mappings.'))
      .finally(() => setLoading(false));
  };

  useEffect(() => { loadRelays(); }, []);

  const handleAdd = async () => {
    const r = parseInt(newRelay, 10);
    const p = parseInt(newPin, 10);
    if (!r || !p) return;
    setAdding(true);
    setAddError(null);
    try {
      await addRelay(r, p);
      setNewRelay('');
      setNewPin('');
      loadRelays();
    } catch (err) {
      setAddError(err.response?.data?.message || err.message);
    } finally {
      setAdding(false);
    }
  };

  const handleDelete = async (relayId) => {
    try {
      await deleteRelay(relayId);
      loadRelays();
    } catch (err) {
      setError(err.response?.data?.message || err.message);
    }
  };

  return (
    <Box>
      <Typography variant="h6" fontWeight={600} gutterBottom>
        Pin / Relay Map
      </Typography>
      <Divider sx={{ mb: 3 }} />

      <Typography variant="body2" color="text.secondary" mb={2}>
        Maps relay numbers to Raspberry Pi GPIO pin numbers. Each zone must have a relay assigned
        before it can physically control the irrigation valve.
      </Typography>

      {loading && <CircularProgress size={24} />}
      {error && <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>{error}</Alert>}

      {!loading && (
        <Stack spacing={3}>
          {relays.length > 0 ? (
            <TableContainer component={Paper} variant="outlined">
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell><strong>Relay</strong></TableCell>
                    <TableCell><strong>GPIO Pin</strong></TableCell>
                    <TableCell><strong>Assigned Zone</strong></TableCell>
                    <TableCell padding="checkbox" />
                  </TableRow>
                </TableHead>
                <TableBody>
                  {relays.map((r) => (
                    <TableRow key={r.relay} hover>
                      <TableCell>{r.relay}</TableCell>
                      <TableCell>{r.pin}</TableCell>
                      <TableCell>
                        {r.zone != null ? (
                          <Typography variant="body2">Zone {r.zone}</Typography>
                        ) : (
                          <Typography variant="body2" color="text.disabled">
                            Unassigned
                          </Typography>
                        )}
                      </TableCell>
                      <TableCell>
                        <Tooltip title="Delete mapping">
                          <IconButton
                            size="small"
                            color="error"
                            onClick={() => handleDelete(r.relay)}
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
            <Alert severity="info">No relay mappings configured.</Alert>
          )}

          {/* Add form */}
          <Paper variant="outlined" sx={{ p: 2 }}>
            <Typography variant="subtitle2" gutterBottom>Add Relay Mapping</Typography>
            {addError && <Alert severity="error" sx={{ mb: 1 }}>{addError}</Alert>}
            <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2} alignItems="flex-start">
              <TextField
                label="Relay #"
                value={newRelay}
                onChange={(e) => setNewRelay(e.target.value)}
                type="number"
                size="small"
                sx={{ width: 120 }}
                inputProps={{ min: 1 }}
              />
              <TextField
                label="GPIO Pin #"
                value={newPin}
                onChange={(e) => setNewPin(e.target.value)}
                type="number"
                size="small"
                sx={{ width: 120 }}
                inputProps={{ min: 1 }}
              />
              <Button
                variant="contained"
                startIcon={<AddIcon />}
                onClick={handleAdd}
                disabled={adding || !newRelay || !newPin}
              >
                {adding ? 'Adding…' : 'Add'}
              </Button>
            </Stack>
          </Paper>
        </Stack>
      )}
    </Box>
  );
}
