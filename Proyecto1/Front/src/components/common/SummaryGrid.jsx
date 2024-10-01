import React from 'react';
import { images } from "../../assets";
import { Box, Grid, Stack, Typography, colors } from '@mui/material';
import Animate from "./Animate";
import MPaper from './MPaper';

const summaryData = [
  {
    title: "Daily income ",
    value: "Q.360.00",
    image: images.summaryImages.totalBook
  },
  {
    title: "Parked Today",
    value: "120",
    image: images.summaryImages.sold
  },
  {
    title: "Parked Outside",
    value: "235",
    image: images.summaryImages.cancel
  }
];

const SummaryGrid = () => {
  return (
    <Grid container spacing={3}>
      {summaryData.map((summary, index) => (
        <Grid key={index} item xs={12} lg={4}>
          <Animate type="fade" delay={(index + 1) / 3}>
            <MPaper>
              <Stack direction="row" alignItems="center" justifyContent="space-between">
                <Stack spacing={1}>
                  <Typography variant="h4" fontWeight="bold">
                    {summary.value}
                  </Typography>
                  <Typography variant="body2" fontWeight="bold" color={colors.grey[600]}>
                    {summary.title}
                  </Typography>
                </Stack>
                <Box sx={{
                  height: "100px",
                  width: "100px",
                  "& img": { width: "100%" }
                }}>
                  <img src={summary.image} alt="summary" />
                </Box>
              </Stack>
            </MPaper>
          </Animate>
        </Grid>
      ))}
    </Grid>
  );
};

export default SummaryGrid;