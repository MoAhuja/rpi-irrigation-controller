import { useState } from 'react';
import { AppBar, Box, CssBaseline, Tab, Tabs, ThemeProvider, Toolbar, Typography, createTheme } from '@mui/material';
import GrassIcon from '@mui/icons-material/Grass';
import DashboardIcon from '@mui/icons-material/Dashboard';
import SettingsIcon from '@mui/icons-material/Settings';
import Dashboard from './pages/Dashboard';
import Admin from './pages/Admin';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#66bb6a' },
    success: { main: '#66bb6a' },
    background: {
      default: '#121212',
      paper: '#1e1e1e',
    },
  },
});

export default function App() {
  const [tab, setTab] = useState(0);
  const [dashboardRefreshKey, setDashboardRefreshKey] = useState(0);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AppBar position="static" color="primary" elevation={2}>
        <Toolbar sx={{ gap: 2 }}>
          <GrassIcon />
          <Typography variant="h6" fontWeight={700} letterSpacing={0.5} sx={{ flexGrow: 1 }}>
            LawnWatcher
          </Typography>
          <Tabs
            value={tab}
            onChange={(_, v) => setTab(v)}
            textColor="inherit"
            TabIndicatorProps={{ style: { backgroundColor: 'white' } }}
            sx={{ minHeight: 64 }}
          >
            <Tab icon={<DashboardIcon fontSize="small" />} iconPosition="start" label="Dashboard" sx={{ minHeight: 64, color: 'rgba(255,255,255,0.85)' }} />
            <Tab icon={<SettingsIcon fontSize="small" />} iconPosition="start" label="Admin" sx={{ minHeight: 64, color: 'rgba(255,255,255,0.85)' }} />
          </Tabs>
        </Toolbar>
      </AppBar>
      <Box component="main">
        {tab === 0 && <Dashboard refreshKey={dashboardRefreshKey} />}
        {tab === 1 && <Admin onDashboardUpdate={() => setDashboardRefreshKey((k) => k + 1)} />}
      </Box>
    </ThemeProvider>
  );
}
