import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom'; // Importa useNavigate
import ChatBubbleOutlineOutlinedIcon from '@mui/icons-material/ChatBubbleOutlineOutlined';
import DashboardCustomizeOutlinedIcon from '@mui/icons-material/DashboardCustomizeOutlined';
import DirectionsCarFilledOutlinedIcon from '@mui/icons-material/DirectionsCarFilledOutlined';
import MailOutlinedIcon from '@mui/icons-material/MailOutlined';
import NotificationsOutlinedIcon from '@mui/icons-material/NotificationsOutlined';
import OtherHousesOutlinedIcon from '@mui/icons-material/OtherHousesOutlined';
import SavingsOutlinedIcon from '@mui/icons-material/SavingsOutlined';
import SportsMotorsportsOutlinedIcon from '@mui/icons-material/SportsMotorsportsOutlined';
import SwapHorizOutlinedIcon from '@mui/icons-material/SwapHorizOutlined';
import CloudOutlinedIcon from '@mui/icons-material/CloudOutlined';
import CameraIcon from '@mui/icons-material/Camera';
import ChatIcon from '@mui/icons-material/Chat';

import InfoOutlinedIcon from '@mui/icons-material/InfoOutlined';
import ExitToAppOutlinedIcon from '@mui/icons-material/ExitToAppOutlined'; // Importa el ícono de logout

import { Box, Drawer, List, ListItem, ListItemButton, ListItemIcon, ListItemText, Paper, Typography, colors } from '@mui/material';
import { images } from "../../assets";
import Animate from "./Animate";

const menus = [
  {
    title: "Dashboard",
    icon: <DashboardCustomizeOutlinedIcon />,
    state: "overview",
    path: "/dashboard" 
  }
];

const serviceMenus = [
  {
    title: "Info",
    icon: <InfoOutlinedIcon />,
    state: "info",
    path: "info" // Agrega la ruta correspondiente
  },
  {
    title: "Weather Control",
    icon: <CloudOutlinedIcon />,
    state: "weather",
    path: "weather" // Agrega la ruta correspondiente
  }
  ,
  {
    title: "Messaging",
    icon: <ChatIcon />,
    state: "messaging",
    path: "messaging" // Agrega la ruta correspondiente
  }  
  ,
  {
    title: "Security Camera",
    icon: <CameraIcon />,
    state: "camera",
    path: "camera" // Agrega la ruta correspondiente
  }  
];

const investmentMenus = [];

const Sidebar = ({ sidebarWidth }) => {
  const navigate = useNavigate(); // Inicializa useNavigate
  const activeState = "overview";

  const handleLogout = () => {
    console.log("User logged out");
    // Redirigir a la página de inicio
    navigate("/");
  };

  const MenuItem = (props) => {
    const handleClick = () => {
      if (props.item.path) {
        navigate(props.item.path); // Navega a la ruta correspondiente
      }
    };

    return (
      <ListItem key={props.index} disableGutters disablePadding sx={{ py: 0.5 }}>
        <ListItemButton 
          onClick={handleClick} // Añade la función handleClick
          sx={{
            borderRadius: "10px",
            bgcolor: props.isActive ? colors.green[600] : "",
            color: props.isActive ? colors.common.white : "",
            "&:hover": {
              bgcolor: props.isActive ? colors.green[600] : "",
              color: props.isActive ? colors.common.white : "",
            }
          }}>
          <ListItemIcon sx={{
            minWidth: "40px",
            color: props.isActive ? colors.common.white : ""
          }}>
            {props.item.icon}
          </ListItemIcon>
          <ListItemText primary={
            <Typography fontWeight={600}>
              {props.item.title}
            </Typography>
          } />
        </ListItemButton>
      </ListItem>
    );
  };

  const drawer = (
    <Box
      padding={3}
      paddingBottom={0}
      display="flex"
      flexDirection="column"
      height="100vh"
      sx={{
        "::-webkit-scrollbar": {
          display: "none"
        }
      }}
    >
      {/* logo */}
      <Box sx={{ textAlign: "center", mb: 2 }}>
        <Animate type="fade" delay={1}>
          <img src={images.logo} alt="logo" height={60} />
        </Animate>
      </Box>
      {/* logo */}

      <Animate sx={{ flexGrow: 1 }}>
        <Paper
          elevation={0}
          square
          sx={{
            borderTopRightRadius: "10px",
            borderTopLeftRadius: "10px",
            p: 2,
            height: "100%",
            boxShadow: "rgba(145, 158, 171, 0.2) 0px 0px 2px 0px, rgba(145, 158, 171, 0.12) 0px 12px 24px -4px"
          }}
        >
          {/* menu group 1 */}
          <List>
            {menus.map((item, index) => (
              <MenuItem
                key={index}
                item={item}
                isActive={item.state === activeState}
              />
            ))}
          </List>
          {/* menu group 1 */}

          {/* menu group 2 */}
          <List>
            <ListItem>
              <Typography fontWeight={600} mt={1} color={colors.grey[600]}>
                Services
              </Typography>
            </ListItem>
            {serviceMenus.map((item, index) => (
              <MenuItem
                key={index}
                item={item}
                isActive={item.state === activeState}
              />
            ))}
          </List>
          {/* menu group 2 */}

          {/* menu group 3 */}
          <List>
            <ListItem>
              {/* Aquí puedes agregar más categorías si es necesario */}
            </ListItem>
            {investmentMenus.map((item, index) => (
              <MenuItem
                key={index}
                item={item}
                isActive={item.state === activeState}
              />
            ))}
          </List>
          {/* menu group 3 */}

          {/* Logout button */}
          <List>
            <ListItem disableGutters disablePadding sx={{ py: 0.5 }}>
              <ListItemButton
                onClick={handleLogout}
                sx={{
                  borderRadius: "10px",
                  bgcolor: colors.red[600],
                  color: colors.common.white,
                  "&:hover": {
                    bgcolor: colors.red[800],
                    color: colors.common.white,
                  }
                }}
              >
                <ListItemIcon sx={{ minWidth: "40px", color: colors.common.white }}>
                  <ExitToAppOutlinedIcon />
                </ListItemIcon>
                <ListItemText primary={
                  <Typography fontWeight={600}>
                    Logout
                  </Typography>
                } />
              </ListItemButton>
            </ListItem>
          </List>
          {/* Logout button */}
        </Paper>
      </Animate>
    </Box>
  );

  return (
    <Box
      component="nav"
      sx={{
        width: { md: sidebarWidth },
        flexShrink: { md: 0 }
      }}
    >
      {/* large screen */}
      <Drawer
        variant="permanent"
        sx={{
          display: { xs: "none", sm: "none", md: "block" },
          "& .MuiDrawer-paper": {
            boxSizing: "border-box",
            width: sidebarWidth,
            borderWidth: 0,
            bgcolor: "transparent",
            "::-webkit-scrollbar": {
              display: "none"
            }
          }
        }}
        open
      >
        {drawer}
      </Drawer>
      {/* large screen */}
    </Box>
  );
};

export default Sidebar;
