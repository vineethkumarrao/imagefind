/**
 * Main App Component
 */

import React, { useState } from "react";
import {
  Container,
  Box,
  AppBar,
  Toolbar,
  Typography,
  CssBaseline,
  ThemeProvider,
  createTheme,
  Switch,
  FormControlLabel,
} from "@mui/material";
import { ImageUpload } from "./components/ImageUpload";
import { AdvancedUpload } from "./components/AdvancedUpload";
import { SearchResults } from "./components/SearchResults";
import { StatsPanel } from "./components/StatsPanel";
import type { UploadResponse } from "./types";

const darkTheme = createTheme({
  palette: {
    mode: "dark",
    primary: {
      main: "#90caf9",
    },
    secondary: {
      main: "#ce93d8",
    },
  },
});

function App() {
  const [searchResults, setSearchResults] = useState<UploadResponse | null>(
    null
  );
  const [advancedMode, setAdvancedMode] = useState(true);

  const handleUploadSuccess = (response: UploadResponse) => {
    setSearchResults(response);
  };

  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <Box sx={{ minHeight: "100vh", bgcolor: "background.default" }}>
        <AppBar position="static" elevation={0}>
          <Toolbar>
            <Typography
              variant="h5"
              component="div"
              sx={{ flexGrow: 1, fontWeight: "bold" }}
            >
              ⚛️ Quantum Image Retrieval
            </Typography>
            <FormControlLabel
              control={
                <Switch
                  checked={advancedMode}
                  onChange={(e) => setAdvancedMode(e.target.checked)}
                  color="secondary"
                />
              }
              label="Advanced Mode"
              sx={{ mr: 2 }}
            />
            <Typography variant="body2" color="text.secondary">
              Powered by AE-QIP Algorithm & Appwrite
            </Typography>
          </Toolbar>
        </AppBar>

        <Container maxWidth="xl" sx={{ py: 4 }}>
          <Box sx={{ textAlign: "center", mb: 4 }}>
            <Typography variant="h3" gutterBottom>
              Quantum-Enhanced Image Search
            </Typography>
            <Typography variant="body1" color="text.secondary">
              Upload an image to find similar images using quantum computing
            </Typography>
          </Box>

          <StatsPanel />

          {advancedMode ? (
            <AdvancedUpload onUploadSuccess={handleUploadSuccess} />
          ) : (
            <ImageUpload onUploadSuccess={handleUploadSuccess} />
          )}

          <SearchResults results={searchResults} />
        </Container>

        <Box
          component="footer"
          sx={{
            py: 3,
            px: 2,
            mt: "auto",
            textAlign: "center",
            borderTop: "1px solid",
            borderColor: "divider",
          }}
        >
          <Typography variant="body2" color="text.secondary">
            Quantum Image Retrieval System © 2025 | ResNet-50 + AE-QIP Algorithm
          </Typography>
        </Box>
      </Box>
    </ThemeProvider>
  );
}

export default App;
