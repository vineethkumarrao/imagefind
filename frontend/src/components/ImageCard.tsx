/**
 * Individual Image Card Component
 */

import React, { useState } from 'react';
import {
  Card,
  CardMedia,
  CardContent,
  Typography,
  Chip,
  LinearProgress,
  Box,
  Dialog,
  IconButton,
} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import { CATEGORY_COLORS, type SimilarImage } from '../types';

interface ImageCardProps {
  image: SimilarImage;
}

export const ImageCard: React.FC<ImageCardProps> = ({ image }) => {
  const [open, setOpen] = useState(false);
  const categoryInfo = CATEGORY_COLORS[image.category] || CATEGORY_COLORS.satellite;
  const similarityPercent = Math.min(100, image.similarity * 100).toFixed(1);

  return (
    <>
      <Card
        sx={{
          height: '100%',
          display: 'flex',
          flexDirection: 'column',
          cursor: 'pointer',
          transition: 'transform 0.2s',
          '&:hover': {
            transform: 'scale(1.05)',
          },
        }}
        onClick={() => setOpen(true)}
      >
        <CardMedia
          component="img"
          height="200"
          image={image.image_url}
          alt={image.filename}
          sx={{ objectFit: 'cover' }}
        />
        <CardContent sx={{ flexGrow: 1 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
            <Chip
              label={categoryInfo.name}
              size="small"
              sx={{
                bgcolor: categoryInfo.color,
                color: 'white',
                mr: 1,
              }}
            />
            <Typography variant="caption" color="text.secondary">
              {categoryInfo.icon}
            </Typography>
          </Box>

          <Typography variant="body2" noWrap title={image.filename}>
            {image.filename}
          </Typography>

          <Box sx={{ mt: 2 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
              <Typography variant="caption" color="text.secondary">
                Similarity
              </Typography>
              <Typography variant="caption" fontWeight="bold">
                {similarityPercent}%
              </Typography>
            </Box>
            <LinearProgress
              variant="determinate"
              value={image.similarity * 100}
              sx={{
                height: 8,
                borderRadius: 4,
                bgcolor: 'grey.200',
                '& .MuiLinearProgress-bar': {
                  bgcolor: image.similarity >= 0.88 ? 'success.main' : 'warning.main',
                },
              }}
            />
          </Box>
        </CardContent>
      </Card>

      <Dialog
        open={open}
        onClose={() => setOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <Box sx={{ position: 'relative' }}>
          <IconButton
            onClick={() => setOpen(false)}
            sx={{
              position: 'absolute',
              right: 8,
              top: 8,
              bgcolor: 'rgba(0,0,0,0.5)',
              color: 'white',
              '&:hover': {
                bgcolor: 'rgba(0,0,0,0.7)',
              },
            }}
          >
            <CloseIcon />
          </IconButton>
          <img
            src={image.image_url}
            alt={image.filename}
            style={{ width: '100%', display: 'block' }}
          />
          <Box sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              {image.filename}
            </Typography>
            <Chip
              label={categoryInfo.name}
              sx={{
                bgcolor: categoryInfo.color,
                color: 'white',
                mr: 1,
              }}
            />
            <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
              Similarity: {similarityPercent}%
            </Typography>
            <Typography variant="caption" color="text.secondary" display="block">
              Image ID: {image.id}
            </Typography>
          </Box>
        </Box>
      </Dialog>
    </>
  );
};

