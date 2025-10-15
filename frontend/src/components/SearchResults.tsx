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
  if (!results) return null;

  return (
    <Box sx={{ width: '100%', maxWidth: 1400, mx: 'auto' }}>
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h5" gutterBottom>
          Search Results
        </Typography>
        
        <Box sx={{ display: 'flex', gap: 2, mb: 2, flexWrap: 'wrap' }}>
          <Chip
            label={`Query: ${results.query_image}`}
            color="primary"
            variant="outlined"
          />
          <Chip
            label={`Total Results: ${results.total_results}`}
            color="info"
          />
          <Chip
            label={`High Confidence: ${results.high_confidence_results}`}
            color="success"
          />
        </Box>

        {results.results.length === 0 ? (
          <Alert severity="info">
            No similar images found. Try uploading a different image.
          </Alert>
        ) : (
          <>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              Showing {results.results.length} similar images with quantum-enhanced similarity scores
            </Typography>

            <Grid container spacing={3}>
              {results.results.map((image) => (
                <Grid item xs={12} sm={6} md={4} lg={3} key={image.document_id}>
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
