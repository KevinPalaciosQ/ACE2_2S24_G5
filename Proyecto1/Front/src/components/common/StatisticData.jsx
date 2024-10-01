import React from 'react';
import MPaper from './MPaper';
import { Box, Stack, Typography, colors } from '@mui/material';
import { Bar } from 'react-chartjs-2';

const chartData = {
  labels: ["Feb", "Mar", "Apr", "May", "Jun", "July", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan"],
  datasets: [
    {
      label: "Incoming",
      data: [150, 130, 160, 180, 200, 170, 160, 150, 140, 180, 200, 210],
      stack: "stack 0",
      backgroundColor: colors.blue[600],
      barPercentage: 0.6,
      categoryPercentage: 0.7
    },
    {
      label: "Outgoing",
      data: [100, 110, 90, 120, 130, 100, 120, 110, 100, 90, 110, 130],
      stack: "stack 1",
      backgroundColor: colors.orange[400],
      barPercentage: 0.6,
      categoryPercentage: 0.7
    }
  ]
};

const charOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    x: {
      grid: { display: false },
      stacked: true
    },
    y: { stacked: true }
  },
  plugins: {
    legend: { display: false },
    title: { display: false }
  },
  elements: {
    bar: {
      borderRadius: 10
    }
  }
};

const StatisticData = () => {
  return (
    <MPaper title="Income Statistics">
      <Stack spacing={4}>
        <Stack direction="row" justifyContent="space-between" alignItems="center">
          <Typography variant="body2">
          (+30% inbound | +15% outbound) compared to last year
          </Typography>
          <Stack direction="row" spacing={3} alignItems="center">
            {chartData.datasets.map((data, index) => (
              <Stack key={index} direction="row" alignItems="center">
                <Box sx={{
                  width: "15px",
                  height: "15px",
                  borderRadius: "4px",
                  bgcolor: data.backgroundColor,
                  mr: 1
                }} />
                <Typography variant="subtitle2">
                  {data.label}
                </Typography>
              </Stack>
            ))}
          </Stack>
        </Stack>
        {/* bar chart */}
        <Box>
          <Bar options={charOptions} data={chartData} height="300px" />
        </Box>
        {/* bar chart */}
      </Stack>
    </MPaper>
  );
};

export default StatisticData;
