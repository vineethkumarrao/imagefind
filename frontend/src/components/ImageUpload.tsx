/**
 * Image Upload Component with Drag & Drop
 * Supports both backend API upload and direct Appwrite upload
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
} from "@mui/material";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import StorageIcon from "@mui/icons-material/Storage";
import SmartToyIcon from "@mui/icons-material/SmartToy";
import { uploadImage, uploadToAppwriteDirect } from "../services/api";
import type { UploadResponse } from "../types";

interface ImageUploadProps {
  onUploadSuccess: (response: UploadResponse) => void;
}

type UploadMode = "backend" | "direct";

export const ImageUpload: React.FC<ImageUploadProps> = ({
  onUploadSuccess,
}) => {
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [uploadMode, setUploadMode] = useState<UploadMode>("backend");
  const [uploadProgress, setUploadProgress] = useState<string>("");

  const onDrop = useCallback(
    async (acceptedFiles: File[]) => {
      if (acceptedFiles.length === 0) return;

      const file = acceptedFiles[0];
      setUploading(true);
      setError(null);
      setUploadProgress("Starting upload...");

      try {
        let response: UploadResponse;

        if (uploadMode === "backend") {
          // Upload via backend API (includes feature extraction and similarity search)
          setUploadProgress("Uploading to backend...");
          response = await uploadImage(file, (progress) => {
            setUploadProgress(`Processing: ${progress}%`);
          });
        } else {
          // Upload directly to Appwrite storage (faster, no backend processing)
          setUploadProgress("Uploading directly to Appwrite...");
          response = await uploadToAppwriteDirect(file, (progress) => {
            setUploadProgress(`Uploading: ${progress}%`);
          });
        }

        setUploadProgress("Upload complete!");
        onUploadSuccess(response);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Upload failed");
        setUploadProgress("");
      } finally {
        setUploading(false);
        setTimeout(() => setUploadProgress(""), 2000);
      }
    },
    [onUploadSuccess, uploadMode]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "image/*": [".png", ".jpg", ".jpeg", ".gif", ".webp"],
    },
    multiple: false,
    disabled: uploading,
  });

  return (
    <Box sx={{ width: "100%", maxWidth: 800, mx: "auto", mb: 4 }}>
      {/* Upload Mode Selector */}
      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          mb: 2,
          gap: 2,
          alignItems: "center",
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
          <ToggleButton value="backend">
            <SmartToyIcon sx={{ mr: 1, fontSize: 18 }} />
            Backend API
          </ToggleButton>
          <ToggleButton value="direct">
            <StorageIcon sx={{ mr: 1, fontSize: 18 }} />
            Direct Upload
          </ToggleButton>
        </ToggleButtonGroup>
      </Box>

      {/* Mode Description */}
      <Box sx={{ textAlign: "center", mb: 2 }}>
        {uploadMode === "backend" ? (
          <Chip
            label="Includes AI feature extraction & similarity search"
            color="primary"
            size="small"
            icon={<SmartToyIcon />}
          />
        ) : (
          <Chip
            label="Fast direct upload to Appwrite storage"
            color="secondary"
            size="small"
            icon={<StorageIcon />}
          />
        )}
      </Box>

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
              {isDragActive ? "Drop image here" : "Upload Image"}
            </Typography>
            <Typography variant="body1" color="text.secondary">
              Drag & drop an image here, or click to select
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
