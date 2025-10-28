/**
 * Main App Component
 */

import { useState } from "react";
import {
  Container,
  Box,
  AppBar,
  Toolbar,
  Typography,
  CssBaseline,
  ThemeProvider,
  createTheme,
} from "@mui/material";
import { ImageUploadNew } from "./components/ImageUploadNew";
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
              Quantum Image Retrieval
            </Typography>
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
              Upload images to find similar ones using quantum computing
            </Typography>
          </Box>

          <StatsPanel />

          <ImageUploadNew onUploadSuccess={handleUploadSuccess} />

          <SearchResults results={searchResults} />
        </Container>
      </Box>
    </ThemeProvider>
  );
}

export default App;
