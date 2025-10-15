/**
 * Statistics Panel Component
 */

import React, { useEffect, useState } from 'react';
import {
  Paper,
  Typography,
  Grid,
  Box,
  Chip,
  CircularProgress,
} from '@mui/material';
import StorageIcon from '@mui/icons-material/Storage';
import CategoryIcon from '@mui/icons-material/Category';
import { getStatistics } from '../services/api';
import type { Statistics } from '../types';
import { CATEGORY_COLORS } from '../types';

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
        <Grid item xs={12} sm={6} md={3}>
          <Box sx={{ textAlign: 'center' }}>
            <Typography variant="h4" color="primary">
              {stats.total_images.toLocaleString()}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Total Images
            </Typography>
          </Box>
        </Grid>

        {Object.entries(stats.categories).map(([category, count]) => {
          const categoryInfo = CATEGORY_COLORS[category];
          return (
            <Grid item xs={12} sm={6} md={3} key={category}>
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="h4" sx={{ color: categoryInfo.color }}>
                  {count.toLocaleString()}
                </Typography>
                <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', mt: 0.5 }}>
                  <Typography variant="body2" color="text.secondary" sx={{ mr: 0.5 }}>
                    {categoryInfo.name}
                  </Typography>
                  <Typography variant="body2">{categoryInfo.icon}</Typography>
                </Box>
              </Box>
            </Grid>
          );
        })}
      </Grid>

      <Box sx={{ mt: 3, display: 'flex', gap: 1, flexWrap: 'wrap' }}>
        <Chip
          icon={<CategoryIcon />}
          label={`Quantum Mode: ${stats.quantum_mode}`}
          size="small"
          color="secondary"
        />
        <Chip
          label={`Feature Dimension: ${stats.feature_dimension}D`}
          size="small"
          variant="outlined"
        />
      </Box>
    </Paper>
  );
};
