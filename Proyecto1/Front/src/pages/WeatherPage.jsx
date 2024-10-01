import React from 'react';
import { Box, Grid, Button, Typography } from '@mui/material';
import Animate from "../components/common/Animate";
import MPaper from '../components/common/MPaper';
import imagen1 from '../assets/images/imagen1.jpg';
import imagen2 from '../assets/images/imagen2.jpg';
import imagen3 from '../assets/images/imagen3.jpg';
import imagen4 from '../assets/images/imagen4.jpg';
import imagen5 from '../assets/images/imagen5.jpg';
import imagen6 from '../assets/images/imagen6.jpg';

// Datos del resumen
const summaryData = [
  { image: imagen1 },
  { image: imagen2 },
  { image: imagen3 },
  { image: imagen4 },
  { image: imagen5 },
  { image: imagen6 }
];

const WeatherPage = () => {
  return (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <Typography 
          variant="h4" 
          align="center" 
          gutterBottom 
          sx={{ 
            backgroundColor: '#FF6F61',  // Color coral
            color: '#fff',                // Texto en blanco
            padding: '16px',              // Espaciado alrededor del texto
            borderRadius: '8px',          // Bordes redondeados
            fontWeight: 'bold',           // Negrita
            boxShadow: 3,                 // Sombra
            textTransform: 'uppercase'     // Texto en mayúsculas
          }}
        >
          Weather Summary
        </Typography>
      </Grid>
      {summaryData.map((summary, index) => (
        <Grid key={index} item xs={12} lg={4}>
          <Animate type="fade" delay={(index + 1) / 3}>
            <MPaper>
              <Box 
                sx={{ 
                  width: '100%', 
                  height: '150px', 
                  display: 'flex', 
                  alignItems: 'center', 
                  justifyContent: 'center' 
                }}
              >
                {/* Imagen ocupando todo el Box */}
                <img src={summary.image} alt={`Imagen ${index + 1}`} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
              </Box>
            </MPaper>
          </Animate>
        </Grid>
      ))}
      <Grid item xs={12} sx={{ textAlign: 'center', mt: 2 }}>
        <Button variant="contained" color="primary">
          Generate Report
        </Button>
      </Grid>
    </Grid>
  );
};

export default WeatherPage;
