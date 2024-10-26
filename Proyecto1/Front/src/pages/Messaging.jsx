import React, { useState } from 'react';
import { Box, Grid, Button, Typography, TextField } from '@mui/material';
import Animate from "../components/common/Animate";
import MPaper from '../components/common/MPaper';

const Messaging = () => {
  const [email, setEmail] = useState('');
  const [subject, setSubject] = useState('');
  const [body, setBody] = useState('');
  const [responseMessage, setResponseMessage] = useState('');

  // Manejar el envío del formulario
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://44.202.22.250:5000/send-email', {  // URL local del backend Flask
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: email,
          subject: subject,
          body: body,
        }),
      });

      const data = await response.json();
      if (response.ok) {
        setResponseMessage(`Correo enviado a: ${email}`);
      } else {
        setResponseMessage(`Error: ${data.error}`);
      }
    } catch (error) {
      setResponseMessage(`Error: ${error.message}`);
    }
  };

  return (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <Typography
          variant="h4"
          align="center"
          gutterBottom
          sx={{
            backgroundColor: '#FF6F61',
            color: '#fff',
            padding: '16px',
            borderRadius: '8px',
            fontWeight: 'bold',
            boxShadow: 3,
            textTransform: 'uppercase',
          }}
        >
          Formulario de Envío de Correos
        </Typography>
      </Grid>

      <Grid item xs={12}>
        <Animate type="fade" delay={0.3}>
          <MPaper>
            <Box
              component="form"
              sx={{
                display: 'flex',
                flexDirection: 'column',
                gap: 2,
                padding: 3,
              }}
              onSubmit={handleSubmit}
            >
              <TextField
                label="Correo Electrónico"
                variant="outlined"
                fullWidth
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
              <TextField
                label="Asunto"
                variant="outlined"
                fullWidth
                required
                value={subject}
                onChange={(e) => setSubject(e.target.value)}
              />
              <TextField
                label="Cuerpo del Mensaje"
                variant="outlined"
                fullWidth
                multiline
                rows={4}
                required
                value={body}
                onChange={(e) => setBody(e.target.value)}
              />

              <Button variant="contained" color="primary" type="submit">
                Enviar Correo
              </Button>

              {responseMessage && (
                <Typography color="secondary" align="center" sx={{ mt: 2 }}>
                  {responseMessage}
                </Typography>
              )}
            </Box>
          </MPaper>
        </Animate>
      </Grid>
    </Grid>
  );
};

export default Messaging;
