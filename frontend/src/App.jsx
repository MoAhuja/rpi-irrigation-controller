import { AppBar, Box, CssBaseline, ThemeProvider, Toolbar, Typography, createTheme } from '@mui/material';
import GrassIcon from '@mui/icons-material/Grass';
import Dashboard from './pages/Dashboard';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: { main: '#2e7d32' },
    success: { main: '#388e3c' },
  },
});

export default function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AppBar position="static" color="primary" elevation={2}>
        <Toolbar>
          <GrassIcon sx={{ mr: 1 }} />
          <Typography variant="h6" fontWeight={700} letterSpacing={0.5}>
            LawnWatcher
          </Typography>
        </Toolbar>
      </AppBar>
      <Box component="main">
        <Dashboard />
      </Box>
    </ThemeProvider>
  );
}
