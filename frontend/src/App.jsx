import { useState } from 'react';
import { AppBar, Box, CssBaseline, Tab, Tabs, ThemeProvider, Toolbar, Tooltip, Typography, createTheme, useMediaQuery } from '@mui/material';
import GrassIcon from '@mui/icons-material/Grass';
import DashboardIcon from '@mui/icons-material/Dashboard';
import SettingsIcon from '@mui/icons-material/Settings';
import Dashboard from './pages/Dashboard';
import Admin from './pages/Admin';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary:   { main: '#2e7d32' },
    secondary: { main: '#0288d1' },
    success:   { main: '#388e3c' },
    warning:   { main: '#f57c00' },
    error:     { main: '#d32f2f' },
    info:      { main: '#0288d1' },
    background: {
      default: '#f0f4f0',
      paper: '#ffffff',
    },
  },
  components: {
    MuiPaper: {
      styleOverrides: {
        root: { backgroundImage: 'none' },
      },
    },
  },
});

export default function App() {
  const [tab, setTab] = useState(0);
  const [dashboardRefreshKey, setDashboardRefreshKey] = useState(0);
  const isMobile = useMediaQuery('(max-width:600px)');

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AppBar position="static" elevation={3} sx={{ background: 'linear-gradient(90deg, #1b5e20 0%, #2e7d32 60%, #0277bd 100%)' }}>
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
            {isMobile ? (
              <>
                <Tooltip title="Dashboard">
                  <Tab icon={<DashboardIcon />} sx={{ minHeight: 64, minWidth: 48, color: 'rgba(255,255,255,0.85)' }} />
                </Tooltip>
                <Tooltip title="Admin">
                  <Tab icon={<SettingsIcon />} sx={{ minHeight: 64, minWidth: 48, color: 'rgba(255,255,255,0.85)' }} />
                </Tooltip>
              </>
            ) : (
              <>
                <Tab icon={<DashboardIcon fontSize="small" />} iconPosition="start" label="Dashboard" sx={{ minHeight: 64, color: 'rgba(255,255,255,0.85)' }} />
                <Tab icon={<SettingsIcon fontSize="small" />} iconPosition="start" label="Admin" sx={{ minHeight: 64, color: 'rgba(255,255,255,0.85)' }} />
              </>
            )}
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
