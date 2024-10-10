import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Box, Button, Grid, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography, Paper, Dialog, DialogTitle, DialogContent, DialogActions, IconButton
} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import Animate from "../components/common/Animate";
import MPaper from '../components/common/MPaper';

const InfoPage = () => {
  const [page, setPage] = useState(0);
  const [selectedBalance, setSelectedBalance] = useState(null);
  const [openDialog, setOpenDialog] = useState(false);
  const [users, setUsers] = useState([]);  
  const [selectedUser, setSelectedUser] = useState(null); 
  const [historial, setHistorial] = useState([]); 
  const rowsPerPage = 3;
  const [hnombre, sethnombre] = useState("");
  const [hapellido, sethapellido] = useState("");
  const [hrfid, sethrfid] = useState("");
  const [huid, setuid] = useState(0);

  useEffect(() => {
    axios.get('http://127.0.0.1:5000/administrador/listarUsuarios')
      .then((response) => {
        if (response.data.status === 200) {
          setUsers(response.data.usuarios);
        } else {
          console.error('Error al obtener usuarios:', response.data.msg);
        }
      })
      .catch((error) => {
        console.error('Error en la solicitud:', error);
      });
  }, []);

  const handleNext = () => {
    if ((page + 1) * rowsPerPage < users.length) {
      setPage(page + 1);
    }
  };

  const handlePrevious = () => {
    if (page > 0) {
      setPage(page - 1);
    }
  };

  const handleSelect = (index) => {
    const user = users[index];
    setSelectedUser(user);
    setSelectedBalance(user.saldo);
    
    axios.post('http://127.0.0.1:5000/administrador/obtenerusuario', {
      uid: user.uid
    })
    .then((response) => {
      if (response.data.status === 200) {
        console.log(response.data)
        setHistorial(response.data.historial);
        sethnombre(response.data.nombre);
        sethapellido(response.data.apellido);
        sethrfid(response.data.rfid);
        setuid(response.data.uid);
        setOpenDialog(true);
      } else {
        console.error('Error al obtener historial:', response.data.msg);
      }
    })
    .catch((error) => {
      console.error('Error en la solicitud:', error);
    });
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
  };

  const handleAdd = () => {
    // Solicitud para sumar saldo
    axios.post('http://127.0.0.1:5000/administrador/sumarSaldo', {
      uid: selectedUser.uid // Aquí se pasa el UID del usuario seleccionado
    })
    .then((response) => {
      if (response.data.status === 200) {
        setSelectedBalance(response.data.saldo); // Actualiza el saldo mostrado
      } else {
        console.error('Error al sumar saldo:', response.data.msg);
      }
    })
    .catch((error) => {
      console.error('Error en la solicitud:', error);
    });
  };

  const handleSubtract = () => {
    // Solicitud para restar saldo
    axios.post('http://127.0.0.1:5000/administrador/restarSaldo', {
      uid: selectedUser.uid // Aquí se pasa el UID del usuario seleccionado
    })
    .then((response) => {
      if (response.data.status === 200) {
        setSelectedBalance(response.data.saldo); // Actualiza el saldo mostrado
      } else {
        console.error('Error al restar saldo:', response.data.msg);
      }
    })
    .catch((error) => {
      console.error('Error en la solicitud:', error);
    });
  };

  return (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <Typography variant="h4" align="center" gutterBottom sx={{ backgroundColor: '#1976d2', color: '#fff', padding: 2, borderRadius: 1 }}>
          User Summary
        </Typography>
      </Grid>

      <Grid item xs={12}>
        <Animate type="fade">
          <MPaper>
            <TableContainer component={Paper} sx={{ boxShadow: 3, borderRadius: 2 }}>
              <Table>
                <TableHead sx={{ backgroundColor: '#1976d2', color: '#fff' }}>
                  <TableRow>
                    <TableCell sx={{ color: '#fff', fontWeight: 'bold' }}>Saldo</TableCell>
                    <TableCell sx={{ color: '#fff', fontWeight: 'bold' }}>Estado</TableCell>
                    <TableCell sx={{ color: '#fff', fontWeight: 'bold' }}>Tipo de Usuario</TableCell>
                    <TableCell sx={{ color: '#fff', fontWeight: 'bold' }}>Seleccionar</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {users.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage).map((user, index) => (
                    <TableRow key={index} sx={{ '&:hover': { backgroundColor: '#e3f2fd' } }}>
                      <TableCell>{`Q.${user.saldo}`}</TableCell>
                      <TableCell>{user.estado}</TableCell>
                      <TableCell>{user.tipoUsuario}</TableCell>
                      <TableCell>
                        <Button 
                          variant="contained" 
                          onClick={() => handleSelect(index)} 
                        >
                          Seleccionar
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </MPaper>
        </Animate>
      </Grid>

      <Grid item xs={12} sx={{ textAlign: 'center', mt: 2 }}>
        <Button variant="contained" onClick={handlePrevious} disabled={page === 0}>
          Previous
        </Button>
        <Button variant="contained" onClick={handleNext} disabled={(page + 1) * rowsPerPage >= users.length} sx={{ ml: 2 }}>
          Next
        </Button>
      </Grid>

      {/* Dialog para ajustar el saldo y mostrar historial */}
      <Dialog open={openDialog} onClose={handleCloseDialog} fullWidth>
        <DialogTitle>
          { 'Usuario'}
          <IconButton
            aria-label="close"
            onClick={handleCloseDialog}
            sx={{ position: 'absolute', right: 8, top: 8, color: (theme) => theme.palette.grey[500] }}
          >
            <CloseIcon />
          </IconButton>
        </DialogTitle>
        <DialogContent>
          {selectedUser && (
            <Box>
              <Typography variant="body1"><strong>Nombre:</strong> {hnombre}</Typography>
              <Typography variant="body1"><strong>Apellido:</strong> {hapellido}</Typography>
              <Typography variant="body1"><strong>UID:</strong> {huid}</Typography>
              <Typography variant="body1"><strong>RFID:</strong> {hrfid}</Typography>
            </Box>
          )}

          <TableContainer component={Paper} sx={{ mt: 2 }}>
            <Table>
              <TableHead sx={{ backgroundColor: '#1976d2', color: '#fff' }}>
                <TableRow>
                  <TableCell sx={{ color: '#fff', fontWeight: 'bold' }}>ID</TableCell>
                  <TableCell sx={{ color: '#fff', fontWeight: 'bold' }}>Fecha</TableCell>
                  <TableCell sx={{ color: '#fff', fontWeight: 'bold' }}>Hora Entrada</TableCell>
                  <TableCell sx={{ color: '#fff', fontWeight: 'bold' }}>Hora Salida</TableCell>
                  <TableCell sx={{ color: '#fff', fontWeight: 'bold' }}>Costo</TableCell>
                  <TableCell sx={{ color: '#fff', fontWeight: 'bold' }}>Tipo Vehículo</TableCell>
                  <TableCell sx={{ color: '#fff', fontWeight: 'bold' }}>Placa</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {historial.map((record, index) => (
                  <TableRow key={index}>
                    <TableCell>{record.id}</TableCell>
                    <TableCell>{record.fecha}</TableCell>
                    <TableCell>{record.horaEntrada}</TableCell>
                    <TableCell>{record.horaSalida}</TableCell>
                    <TableCell>{record.costo}</TableCell>
                    <TableCell>{record.tipoVehiculo}</TableCell>
                    <TableCell>{record.placa}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>

          <Typography variant="body1" sx={{ mt: 2 }}><strong>Saldo:</strong> Q.{selectedBalance}</Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleSubtract} variant="contained" sx={{ backgroundColor: '#f44336', '&:hover': { backgroundColor: '#d32f2f' } }}>
            -
          </Button>
          <Button onClick={handleAdd} variant="contained" sx={{ backgroundColor: '#4caf50', '&:hover': { backgroundColor: '#388e3c' } }}>
            +
          </Button>
        </DialogActions>
      </Dialog>
    </Grid>
  );
};

export default InfoPage;
