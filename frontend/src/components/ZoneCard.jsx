import {
  Box,
  Button,
  Card,
  CardActions,
  CardContent,
  Chip,
  Divider,
  Stack,
  Tooltip,
  Typography,
} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import StopIcon from '@mui/icons-material/Stop';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import HistoryIcon from '@mui/icons-material/History';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import CancelIcon from '@mui/icons-material/Cancel';
import WaterDropIcon from '@mui/icons-material/WaterDrop';
import TimelineIcon from '@mui/icons-material/Timeline';

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

export default function ZoneCard({ zone, onStart, onStop, onEdit, onHistory }) {
  const { id, name, description, enabled, is_running, last_run, next_run } = zone;

  return (
    <Card
      elevation={is_running ? 6 : 2}
      sx={{
        borderLeft: 6,
        borderColor: is_running ? 'success.main' : enabled ? 'primary.main' : 'grey.400',
        background: is_running
          ? 'linear-gradient(135deg, #e8f5e9 0%, #f1f8e9 100%)'
          : enabled
          ? 'linear-gradient(135deg, #f3f8ff 0%, #e8f4fd 100%)'
          : 'linear-gradient(135deg, #f5f5f5 0%, #eeeeee 100%)',
        transition: 'box-shadow 0.3s',
      }}
    >
      <CardContent>
        {/* Header row */}
        <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={1}>
          <Box>
            <Typography variant="h6" fontWeight={600}>
              {name}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {description}
            </Typography>
          </Box>
          <Stack direction="row" spacing={1} alignItems="center">
            {/* Enabled status — always visible */}
            <Chip
              size="small"
              icon={enabled ? <CheckCircleIcon /> : <CancelIcon />}
              label={enabled ? 'Enabled' : 'Disabled'}
              color={enabled ? 'primary' : 'default'}
              variant={enabled ? 'filled' : 'outlined'}
            />
            {/* Running status — always visible */}
            <Chip
              size="small"
              icon={<WaterDropIcon />}
              label={is_running ? 'Running' : 'Idle'}
              color={is_running ? 'success' : 'default'}
              variant={is_running ? 'filled' : 'outlined'}
            />
          </Stack>
        </Box>

        <Divider sx={{ my: 1 }} />

        {/* Schedule info */}
        <Stack direction="row" spacing={3}>
          <Box display="flex" alignItems="center" gap={1}>
            <AccessTimeIcon fontSize="small" color="action" />
            <Typography variant="body2">
              <strong>Next run:</strong> {next_run ? formatDateTime(next_run.start) : 'N/A'}
            </Typography>
          </Box>
          <Box display="flex" alignItems="center" gap={1}>
            <HistoryIcon fontSize="small" color="action" />
            <Typography variant="body2">
              <strong>Last run:</strong> {last_run ? formatDateTime(last_run.start) : 'N/A'}
            </Typography>
          </Box>
        </Stack>
      </CardContent>

      <CardActions sx={{ justifyContent: 'flex-end', px: 2, pb: 2, gap: 1 }}>
        <Tooltip title="Edit zone">
          <Button
            size="small"
            variant="outlined"
            startIcon={<EditIcon />}
            onClick={() => onEdit(id)}
          >
            Edit
          </Button>
        </Tooltip>

        <Tooltip title="View run history">
          <Button
            size="small"
            variant="outlined"
            startIcon={<TimelineIcon />}
            onClick={() => onHistory(zone)}
          >
            History
          </Button>
        </Tooltip>

        {is_running ? (
          <Button
            size="small"
            variant="contained"
            color="error"
            startIcon={<StopIcon />}
            onClick={() => onStop(id)}
          >
            Stop
          </Button>
        ) : (
          <Button
            size="small"
            variant="contained"
            color="success"
            startIcon={<PlayArrowIcon />}
            onClick={() => onStart(zone)}
            disabled={!enabled}
          >
            Start
          </Button>
        )}
      </CardActions>
    </Card>
  );
}
