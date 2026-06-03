import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  InputAdornment,
  TextField,
} from '@mui/material';
import { useState } from 'react';

export default function StartZoneDialog({ open, zoneName, onConfirm, onCancel }) {
  const [duration, setDuration] = useState(10);
  const [error, setError] = useState('');

  const handleConfirm = () => {
    const val = parseInt(duration, 10);
    if (!val || val < 1) {
      setError('Duration must be at least 1 minute');
      return;
    }
    onConfirm(val);
    setDuration(10);
    setError('');
  };

  const handleCancel = () => {
    setDuration(10);
    setError('');
    onCancel();
  };

  return (
    <Dialog open={open} onClose={handleCancel} maxWidth="xs" fullWidth>
      <DialogTitle>Start Zone — {zoneName}</DialogTitle>
      <DialogContent>
        <TextField
          autoFocus
          margin="dense"
          label="Duration"
          type="number"
          fullWidth
          value={duration}
          onChange={(e) => {
            setDuration(e.target.value);
            setError('');
          }}
          InputProps={{
            endAdornment: <InputAdornment position="end">minutes</InputAdornment>,
            inputProps: { min: 1 },
          }}
          error={!!error}
          helperText={error}
        />
      </DialogContent>
      <DialogActions>
        <Button onClick={handleCancel}>Cancel</Button>
        <Button onClick={handleConfirm} variant="contained" color="success">
          Start
        </Button>
      </DialogActions>
    </Dialog>
  );
}
