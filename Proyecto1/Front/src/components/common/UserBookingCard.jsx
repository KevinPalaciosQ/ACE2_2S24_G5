import React from 'react';
import MPaper from './MPaper';
import { Avatar, Box, Stack, Typography, colors } from '@mui/material';
import { images } from '../../assets';
import CalendarMonthOutlinedIcon from '@mui/icons-material/CalendarMonthOutlined';
import PeopleAltOutlinedIcon from '@mui/icons-material/PeopleAltOutlined';

const UserBookingCard = () => {
  return (
    <MPaper title="Latest guard">
      <Stack spacing={3}>
        {/* user info */}
        <Stack direction="row" spacing={2}>
          <Avatar alt="user" src={images.userProfile} />
          <Stack justifyContent="space-between">
            <Typography variant="subtitle2">
              Bruce Lee
            </Typography>
            <Typography variant="caption" color={colors.grey[500]}>
              28 Sep 2024 09:50
            </Typography>
          </Stack>
        </Stack>
        {/* user info */}

        {/* booking info */}

        {/* booking info */}

        {/* image */}
        <Box sx={{
          pt: "100%",
          position: "relative",
          "& img": {
            position: "absolute",
            top: 0,
            height: "100%",
            width: "100%",
            borderRadius: 8
          }
        }}>
          <img src={images.bookingImage} alt="booking" />
        </Box>
        {/* image */}
      </Stack>
    </MPaper>
  );
};

export default UserBookingCard;