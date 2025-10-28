/**
 * Advanced Upload Component with Category Selection and Upload Mode
 * Supports backend API upload with Cloudinary storage and Pinecone indexing
 */

import React, { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import {
  Box,
  Paper,
  Typography,
  CircularProgress,
  Alert,
  ToggleButtonGroup,
  ToggleButton,
  LinearProgress,
  Chip,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  SelectChangeEvent,
  Stack,
} from "@mui/material";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import StorageIcon from "@mui/icons-material/Storage";
import SmartToyIcon from "@mui/icons-material/SmartToy";
import LocalHospitalIcon from "@mui/icons-material/LocalHospital";
import SatelliteIcon from "@mui/icons-material/Satellite";
import VideocamIcon from "@mui/icons-material/Videocam";
import {
  uploadImage,
  uploadAndStore,
} from "../services/api";
import type { UploadResponse } from "../types";

interface AdvancedUploadProps {
  onUploadSuccess: (response: UploadResponse) => void;
}

type UploadMode = "search" | "store";
type Category = "healthcare" | "satellite" | "surveillance";

const CATEGORY_ICONS = {
  healthcare: <LocalHospitalIcon />,
  satellite: <SatelliteIcon />,
  surveillance: <VideocamIcon />,
};

export const AdvancedUpload: React.FC<AdvancedUploadProps> = ({
  onUploadSuccess,
}) => {
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [uploadMode, setUploadMode] = useState<UploadMode>("search");
  const [category, setCategory] = useState<Category>("healthcare");
  const [uploadProgress, setUploadProgress] = useState<string>("");

  const handleCategoryChange = (event: SelectChangeEvent) => {
    setCategory(event.target.value as Category);
  };

  const onDrop = useCallback(
    async (acceptedFiles: File[]) => {
      if (acceptedFiles.length === 0) return;

      setUploading(true);
      setError(null);
      setUploadProgress(`Starting upload of ${acceptedFiles.length} image(s)...`);

      try {
        // Process all files
        for (let i = 0; i < acceptedFiles.length; i++) {
          const file = acceptedFiles[i];
          setUploadProgress(`Processing image ${i + 1} of ${acceptedFiles.length}...`);

          let response: UploadResponse;

          if (uploadMode === "search") {
            // Upload via backend API for similarity search only (no storage)
            setUploadProgress(`Uploading image ${i + 1} to backend...`);
            response = await uploadImage(file, (progress) => {
              setUploadProgress(`Image ${i + 1}: Processing ${progress}%`);
            });
          } else {
            // Upload and store in Cloudinary + index in Pinecone with category
            setUploadProgress(`Uploading and storing image ${i + 1}...`);
            response = await uploadAndStore(file, category, (progress) => {
              setUploadProgress(`Image ${i + 1}: Storing ${progress}%`);
            });
          }

          // Only show results for the last image
          if (i === acceptedFiles.length - 1) {
            setUploadProgress("All uploads complete!");
            onUploadSuccess(response);
          }
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : "Upload failed");
        setUploadProgress("");
      } finally {
        setUploading(false);
        setTimeout(() => setUploadProgress(""), 2000);
      }
    },
    [onUploadSuccess, uploadMode, category]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "image/*": [".png", ".jpg", ".jpeg", ".gif", ".webp"],
    },
    multiple: true,
    disabled: uploading,
  });

  const getModeDescription = () => {
    switch (uploadMode) {
      case "search":
        return "Search for similar images without storing";
      case "store":
        return "Upload to Cloudinary, index in Pinecone, and search similar";
      default:
        return "";
    }
  };

  return (
    <Box sx={{ width: "100%", maxWidth: 900, mx: "auto", mb: 4 }}>
      {/* Upload Mode Selector */}
      <Stack spacing={2} sx={{ mb: 3 }}>
        <Box
          sx={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            gap: 2,
          }}
        >
          <Typography variant="body2" color="text.secondary">
            Upload Method:
          </Typography>
          <ToggleButtonGroup
            value={uploadMode}
            exclusive
            onChange={(_, newMode) => newMode && setUploadMode(newMode)}
            size="small"
            disabled={uploading}
          >
            <ToggleButton value="search">
              <SmartToyIcon sx={{ mr: 1, fontSize: 18 }} />
              Search Only
            </ToggleButton>
            <ToggleButton value="store">
              <StorageIcon sx={{ mr: 1, fontSize: 18 }} />
              Store & Search
            </ToggleButton>
          </ToggleButtonGroup>
        </Box>

        {/* Category Selector (only for store mode) */}
        {uploadMode === "store" && (
          <Box sx={{ display: "flex", justifyContent: "center" }}>
            <FormControl size="small" sx={{ minWidth: 200 }}>
              <InputLabel>Category</InputLabel>
              <Select
                value={category}
                label="Category"
                onChange={handleCategoryChange}
                disabled={uploading}
              >
                <MenuItem value="healthcare">
                  <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                    {CATEGORY_ICONS.healthcare}
                    Healthcare
                  </Box>
                </MenuItem>
                <MenuItem value="satellite">
                  <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                    {CATEGORY_ICONS.satellite}
                    Satellite
                  </Box>
                </MenuItem>
                <MenuItem value="surveillance">
                  <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                    {CATEGORY_ICONS.surveillance}
                    Surveillance
                  </Box>
                </MenuItem>
              </Select>
            </FormControl>
          </Box>
        )}

        {/* Mode Description */}
        <Box sx={{ textAlign: "center" }}>
          <Chip
            label={getModeDescription()}
            color={uploadMode === "search" ? "primary" : "secondary"}
            size="small"
          />
        </Box>
      </Stack>

      {/* Upload Area */}
      <Paper
        {...getRootProps()}
        sx={{
          p: 6,
          textAlign: "center",
          cursor: uploading ? "wait" : "pointer",
          border: "2px dashed",
          borderColor: isDragActive ? "primary.main" : "grey.400",
          bgcolor: isDragActive ? "action.hover" : "background.paper",
          transition: "all 0.3s",
          "&:hover": {
            borderColor: "primary.main",
            bgcolor: "action.hover",
          },
        }}
      >
        <input {...getInputProps()} />

        {uploading ? (
          <Box>
            <CircularProgress size={60} />
            <Typography variant="h6" sx={{ mt: 2 }}>
              {uploadProgress || "Processing image..."}
            </Typography>
            <LinearProgress sx={{ mt: 2, maxWidth: 400, mx: "auto" }} />
          </Box>
        ) : (
          <Box>
            <CloudUploadIcon
              sx={{ fontSize: 60, color: "primary.main", mb: 2 }}
            />
            <Typography variant="h5" gutterBottom>
              {isDragActive ? "Drop images here" : "Upload Images"}
            </Typography>
            <Typography variant="body1" color="text.secondary">
              Drag & drop images here, or click to select multiple images
            </Typography>
            <Typography
              variant="caption"
              color="text.secondary"
              display="block"
              sx={{ mt: 1 }}
            >
              Supports: PNG, JPG, JPEG, GIF, WebP
            </Typography>
          </Box>
        )}
      </Paper>

      {error && (
        <Alert severity="error" sx={{ mt: 2 }}>
          {error}
        </Alert>
      )}
    </Box>
  );
};
