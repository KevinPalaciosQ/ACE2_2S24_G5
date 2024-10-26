import React, { useRef, useState, useEffect } from 'react';
import { Box, Grid, Typography } from '@mui/material';
import Animate from "../components/common/Animate";
import MPaper from '../components/common/MPaper';

const Camera = () => {
  const videoRef = useRef(null);
  const [isStreaming, setIsStreaming] = useState(false);

  // Conectar al stream de video de la cámara del dispositivo al cargar el componente
  useEffect(() => {
    const startStreaming = async () => {
      if (videoRef.current) {
        try {
          const stream = await navigator.mediaDevices.getUserMedia({ video: true });
          videoRef.current.srcObject = stream;
          videoRef.current.play();
          setIsStreaming(true);
        } catch (err) {
          console.error("Error accessing the camera: ", err);
        }
      }
    };

    startStreaming();
  }, []); // Solo se ejecuta una vez al montar el componente

  return (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <Typography
          variant="h4"
          align="center"
          gutterBottom
          sx={{
            backgroundColor: '#1976d2',
            color: '#fff',
            padding: 2,
            borderRadius: 1,
          }}
        >
          Cámara de Seguridad
        </Typography>
      </Grid>
      <Grid item xs={12}>
        <Animate type="fade">
          <MPaper>
            <Box
              sx={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                padding: 3,
              }}
            >
              {/* Elemento de Video */}
              <video
                ref={videoRef}
                width="100%"
                height="auto"
                style={{ borderRadius: '8px', boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)' }}
                autoPlay
                muted
              >
                {/* Mensaje si el navegador no soporta el video */}
                Your browser does not support the video tag.
              </video>
            </Box>
          </MPaper>
        </Animate>
      </Grid>
    </Grid>
  );
};

export default Camera;
