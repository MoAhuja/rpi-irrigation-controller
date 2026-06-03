import { Box, Divider, Paper, Stack, Typography } from '@mui/material';
import PowerSettingsNewIcon from '@mui/icons-material/PowerSettingsNew';
import WaterDropIcon from '@mui/icons-material/WaterDrop';
import CloudIcon from '@mui/icons-material/Cloud';
import NotificationsIcon from '@mui/icons-material/Notifications';
import CableIcon from '@mui/icons-material/Cable';

import SystemControlPanel from '../components/admin/SystemControlPanel';
import RainDelayPanel from '../components/admin/RainDelayPanel';
import WeatherPanel from '../components/admin/WeatherPanel';
import NotificationsPanel from '../components/admin/NotificationsPanel';
import RelayMapPanel from '../components/admin/RelayMapPanel';

const SECTIONS = [
  { key: 'system',        icon: <PowerSettingsNewIcon />, component: SystemControlPanel },
  { key: 'raindelay',     icon: <WaterDropIcon />,        component: RainDelayPanel },
  { key: 'weather',       icon: <CloudIcon />,            component: WeatherPanel },
  { key: 'notifications', icon: <NotificationsIcon />,    component: NotificationsPanel },
  { key: 'relays',        icon: <CableIcon />,            component: RelayMapPanel },
];

export default function Admin({ onDashboardUpdate }) {
  return (
    <Box sx={{ p: { xs: 2, md: 4 }, maxWidth: 800, mx: 'auto' }}>
      <Stack spacing={3}>
        {SECTIONS.map(({ key, component: Panel }, i) => (
          <Paper key={key} elevation={1} sx={{ borderRadius: 2, overflow: 'hidden' }}>
            <Box sx={{ p: { xs: 2, md: 3 } }}>
              <Panel onDashboardUpdate={onDashboardUpdate} />
            </Box>
            {i < SECTIONS.length - 1 && <Divider />}
          </Paper>
        ))}
      </Stack>
    </Box>
  );
}

