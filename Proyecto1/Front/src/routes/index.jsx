import { createBrowserRouter } from "react-router-dom";
import AppLayout from "../components/layout/AppLayout";
import LoginPage from "../pages/LoginPage";
import MainLayout from "../components/layout/MainLayout";
import DashboardPage from "../pages/DashboardPage";
import WeatherPage from "../pages/WeatherPage";  
import InfoPage from "../pages/InfoPage";  
import Messaging from "../pages/Messaging";
import Camera from "../pages/Camera";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <AppLayout />,
    children: [
      {
        index: true,
        element: <LoginPage />
      },
      {
        path: "dashboard",
        element: <MainLayout />,
        children: [
          {
            index: true,
            element: <DashboardPage />
          },
          {
            path: "weather",  
            element: <WeatherPage />
          },
          {
            path: "info",  
            element: <InfoPage />
          },
          {
            path: "messaging",  
            element: <Messaging />
          },
          {
            path: "camera",  
            element: <Camera />
          },          
        ]
      }
    ]
  }
]);
