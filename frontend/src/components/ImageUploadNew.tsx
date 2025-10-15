/**
 * Improved Image Upload Component
 * Supports: Search mode and Upload mode with multiple files
 */

import React, { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import {
  Box,
  Paper,
  Typography,
  CircularProgress,
  Alert,
  Button,
  LinearProgress,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  SelectChangeEvent,
  Stack,
  Chip,
  Grid,
  Card,
  CardMedia,
  CardContent,
  IconButton,
} from "@mui/material";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import SearchIcon from "@mui/icons-material/Search";
import DeleteIcon from "@mui/icons-material/Delete";
import FolderOpenIcon from "@mui/icons-material/FolderOpen";
import { uploadImage, uploadAndStore } from "../services/api";
import type { UploadResponse } from "../types";

interface ImageUploadNewProps {
  onUploadSuccess: (response: UploadResponse) => void;
}

type UploadMode = "search" | "upload";
type Category = "healthcare" | "satellite" | "surveillance";

const CATEGORY_LABELS = {
  healthcare: "Healthcare",
  satellite: "Satellite",
  surveillance: "Surveillance",
};

interface FilePreview {
  file: File;
  preview: string;
  status: "pending" | "uploading" | "success" | "error";
  progress: number;
  error?: string;
}

export const ImageUploadNew: React.FC<ImageUploadNewProps> = ({
  onUploadSuccess,
}) => {
  const [mode, setMode] = useState<UploadMode>("search");
  const [category, setCategory] = useState<Category>("healthcare");
  const [files, setFiles] = useState<FilePreview[]>([]);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleCategoryChange = (event: SelectChangeEvent) => {
    setCategory(event.target.value as Category);
  };

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const newFiles: FilePreview[] = acceptedFiles.map((file) => ({
      file,
      preview: URL.createObjectURL(file),
      status: "pending",
      progress: 0,
    }));

    setFiles((prev) => [...prev, ...newFiles]);
    setError(null);
  }, []);

  const { getRootProps, getInputProps, isDragActive, open } = useDropzone({
    onDrop,
    accept: {
      "image/*": [".png", ".jpg", ".jpeg", ".gif", ".webp"],
    },
    multiple: true,
    noClick: true,
  });

  const removeFile = (index: number) => {
    setFiles((prev) => {
      const newFiles = [...prev];
      URL.revokeObjectURL(newFiles[index].preview);
      newFiles.splice(index, 1);
      return newFiles;
    });
  };

  const uploadFiles = async () => {
    if (files.length === 0) return;

    setUploading(true);
    setError(null);

    try {
      for (let i = 0; i < files.length; i++) {
        const filePreview = files[i];

        // Update status to uploading
        setFiles((prev) => {
          const newFiles = [...prev];
          newFiles[i].status = "uploading";
          return newFiles;
        });

        try {
          let response: UploadResponse;

          if (mode === "search") {
            // Search mode - just find similar images
            response = await uploadImage(filePreview.file, (progress) => {
              setFiles((prev) => {
                const newFiles = [...prev];
                newFiles[i].progress = progress;
                return newFiles;
              });
            });
          } else {
            // Upload mode - store in Appwrite with category
            response = await uploadAndStore(
              filePreview.file,
              category,
              (progress) => {
                setFiles((prev) => {
                  const newFiles = [...prev];
                  newFiles[i].progress = progress;
                  return newFiles;
                });
              }
            );
          }

          // Update status to success
          setFiles((prev) => {
            const newFiles = [...prev];
            newFiles[i].status = "success";
            newFiles[i].progress = 100;
            return newFiles;
          });

          // Call success callback for the last file
          if (i === files.length - 1) {
            onUploadSuccess(response);
          }
        } catch (err) {
          // Update status to error
          setFiles((prev) => {
            const newFiles = [...prev];
            newFiles[i].status = "error";
            newFiles[i].error =
              err instanceof Error ? err.message : "Upload failed";
            return newFiles;
          });
        }
      }
    } finally {
      setUploading(false);
    }
  };

  const clearAll = () => {
    files.forEach((f) => URL.revokeObjectURL(f.preview));
    setFiles([]);
    setError(null);
  };

  return (
    <Box sx={{ width: "100%" }}>
      {/* Mode Selection */}
      <Stack direction="row" spacing={2} sx={{ mb: 3 }}>
        <Button
          variant={mode === "search" ? "contained" : "outlined"}
          startIcon={<SearchIcon />}
          onClick={() => setMode("search")}
          fullWidth
        >
          Search Only
        </Button>
        <Button
          variant={mode === "upload" ? "contained" : "outlined"}
          startIcon={<CloudUploadIcon />}
          onClick={() => setMode("upload")}
          fullWidth
        >
          Upload & Store
        </Button>
      </Stack>

      {/* Category Selection (only for upload mode) */}
      {mode === "upload" && (
        <FormControl fullWidth sx={{ mb: 3 }}>
          <InputLabel>Category</InputLabel>
          <Select value={category} onChange={handleCategoryChange} label="Category">
            {Object.entries(CATEGORY_LABELS).map(([value, label]) => (
              <MenuItem key={value} value={value}>
                {label}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      )}

      {/* Dropzone */}
      <Paper
        {...getRootProps()}
        sx={{
          p: 4,
          border: "2px dashed",
          borderColor: isDragActive ? "primary.main" : "grey.300",
          bgcolor: isDragActive ? "action.hover" : "background.paper",
          cursor: "pointer",
          transition: "all 0.3s",
          "&:hover": {
            borderColor: "primary.main",
            bgcolor: "action.hover",
          },
        }}
      >
        <input {...getInputProps()} />
        <Box sx={{ textAlign: "center" }}>
          <CloudUploadIcon sx={{ fontSize: 48, color: "primary.main", mb: 2 }} />
          <Typography variant="h6" gutterBottom>
            {isDragActive
              ? "Drop the images here"
              : "Drag & drop images here"}
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            or
          </Typography>
          <Stack direction="row" spacing={2} justifyContent="center">
            <Button variant="outlined" onClick={open}>
              Select Files
            </Button>
            <Button variant="outlined" startIcon={<FolderOpenIcon />} onClick={open}>
              Select Folder
            </Button>
          </Stack>
          <Typography variant="caption" color="text.secondary" sx={{ mt: 2, display: "block" }}>
            Supports: PNG, JPG, JPEG, GIF, WebP (Multiple files allowed)
          </Typography>
        </Box>
      </Paper>

      {/* Error Message */}
      {error && (
        <Alert severity="error" sx={{ mt: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {/* File Previews */}
      {files.length > 0 && (
        <Box sx={{ mt: 3 }}>
          <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 2 }}>
            <Typography variant="h6">
              Selected Files ({files.length})
            </Typography>
            <Stack direction="row" spacing={1}>
              <Button
                variant="contained"
                onClick={uploadFiles}
                disabled={uploading}
                startIcon={
                  uploading ? <CircularProgress size={20} /> : mode === "search" ? <SearchIcon /> : <CloudUploadIcon />
                }
              >
                {uploading
                  ? "Processing..."
                  : mode === "search"
                  ? "Search Similar"
                  : "Upload All"}
              </Button>
              <Button variant="outlined" onClick={clearAll} disabled={uploading}>
                Clear All
              </Button>
            </Stack>
          </Stack>

          <Grid container spacing={2}>
            {files.map((filePreview, index) => (
              <Grid item xs={12} sm={6} md={4} lg={3} key={index}>
                <Card>
                  <CardMedia
                    component="img"
                    height="140"
                    image={filePreview.preview}
                    alt={filePreview.file.name}
                    sx={{ objectFit: "cover" }}
                  />
                  <CardContent>
                    <Typography variant="body2" noWrap title={filePreview.file.name}>
                      {filePreview.file.name}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      {(filePreview.file.size / 1024).toFixed(1)} KB
                    </Typography>

                    {/* Status */}
                    <Box sx={{ mt: 1 }}>
                      {filePreview.status === "pending" && (
                        <Chip label="Pending" size="small" color="default" />
                      )}
                      {filePreview.status === "uploading" && (
                        <>
                          <LinearProgress
                            variant="determinate"
                            value={filePreview.progress}
                            sx={{ mb: 1 }}
                          />
                          <Chip
                            label={`${filePreview.progress}%`}
                            size="small"
                            color="primary"
                          />
                        </>
                      )}
                      {filePreview.status === "success" && (
                        <Chip label="Success" size="small" color="success" />
                      )}
                      {filePreview.status === "error" && (
                        <Chip label="Error" size="small" color="error" />
                      )}
                    </Box>

                    {filePreview.error && (
                      <Typography variant="caption" color="error" sx={{ mt: 1, display: "block" }}>
                        {filePreview.error}
                      </Typography>
                    )}
                  </CardContent>
                  <IconButton
                    size="small"
                    onClick={() => removeFile(index)}
                    disabled={uploading}
                    sx={{ position: "absolute", top: 8, right: 8, bgcolor: "background.paper" }}
                  >
                    <DeleteIcon />
                  </IconButton>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Box>
      )}
    </Box>
  );
};
