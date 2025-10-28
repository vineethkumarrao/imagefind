/**
 * Statistics Panel Component
 */

import React, { useEffect, useState } from 'react';
import {
  Paper,
  Typography,
  Grid,
  Box,
  CircularProgress,
} from '@mui/material';
import StorageIcon from '@mui/icons-material/Storage';
import { getStatistics } from '../services/api';
import type { Statistics } from '../types';

export const StatsPanel: React.FC = () => {
  const [stats, setStats] = useState<Statistics | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await getStatistics();
        setStats(response.statistics);
      } catch (error) {
        console.error('Failed to fetch statistics:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (!stats) return null;

  return (
    <Paper sx={{ p: 3, mb: 3 }}>
      <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
        <StorageIcon sx={{ mr: 1 }} />
        Database Statistics
      </Typography>

      <Grid container spacing={2} sx={{ mt: 1 }}>
        <Grid item xs={12} sm={6} md={4}>
          <Box sx={{ textAlign: 'center' }}>
            <Typography variant="h4" color="primary">
              {stats.total_vector_count.toLocaleString()}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Total Vectors
            </Typography>
          </Box>
        </Grid>

        <Grid item xs={12} sm={6} md={4}>
          <Box sx={{ textAlign: 'center' }}>
            <Typography variant="h4" color="primary">
              {stats.dimension}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Feature Dimension
            </Typography>
          </Box>
        </Grid>

        <Grid item xs={12} sm={6} md={4}>
          <Box sx={{ textAlign: 'center' }}>
            <Typography variant="body1" sx={{ fontWeight: 'bold', color: 'primary.main' }}>
              {stats.index_name}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Index Name
            </Typography>
          </Box>
        </Grid>
      </Grid>
    </Paper>
  );
};

export default StatsPanel;
