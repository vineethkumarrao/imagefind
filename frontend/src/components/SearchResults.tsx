/**
 * Search Results Component
 */

import React from 'react';
import {
  Box,
  Typography,
  Grid,
  Paper,
  Chip,
  Alert,
} from '@mui/material';
import { ImageCard } from './ImageCard';
import type { UploadResponse } from '../types';

interface SearchResultsProps {
  results: UploadResponse | null;
}

export const SearchResults: React.FC<SearchResultsProps> = ({ results }) => {
  if (!results || !results.similar_images) return null;

  return (
    <Box sx={{ width: '100%', maxWidth: 1400, mx: 'auto' }}>
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h5" gutterBottom>
          Search Results
        </Typography>
        
        <Box sx={{ display: 'flex', gap: 2, mb: 2, flexWrap: 'wrap' }}>
          {results.uploaded_image && (
            <Chip
              label={`Uploaded: ${results.uploaded_image.filename}`}
              color="primary"
              variant="outlined"
            />
          )}
          <Chip
            label={`Total Similar: ${results.similar_images.length}`}
            color="info"
          />
        </Box>

        {results.similar_images.length === 0 ? (
          <Alert severity="info">
            No similar images found. Try uploading a different image.
          </Alert>
        ) : (
          <>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              Showing {results.similar_images.length} similar images
            </Typography>

            <Grid container spacing={3}>
              {results.similar_images.map((image) => (
                <Grid item xs={12} sm={6} md={4} lg={3} key={image.id}>
                  <ImageCard image={image} />
                </Grid>
              ))}
            </Grid>
          </>
        )}
      </Paper>
    </Box>
  );
};
