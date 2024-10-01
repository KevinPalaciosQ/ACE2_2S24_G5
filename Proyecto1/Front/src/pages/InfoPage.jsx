import React, { useState } from 'react';
import { Box, Button, Grid, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography, Paper } from '@mui/material';
import Animate from "../components/common/Animate";
import MPaper from '../components/common/MPaper';

// Datos de ejemplo para la tabla
const data = [
  { firstName: 'John', lastName: 'Doe', uid: '001', model: 'Model A' },
  { firstName: 'Jane', lastName: 'Smith', uid: '002', model: 'Model B' },
  { firstName: 'Alice', lastName: 'Johnson', uid: '003', model: 'Model C' },
  { firstName: 'Bob', lastName: 'Brown', uid: '004', model: 'Model D' },
  { firstName: 'Charlie', lastName: 'Davis', uid: '005', model: 'Model E' },
  { firstName: 'David', lastName: 'Wilson', uid: '006', model: 'Model F' },
];

// Datos de ejemplo para el resumen
const resumeData = [
  { balance: '1000 USD', status: 'Active', userType: 'Admin' },
  { balance: '500 USD', status: 'Inactive', userType: 'User' },
  { balance: '750 USD', status: 'Active', userType: 'Guest' },
];

const InfoPage = () => {
  const [page, setPage] = useState(0);
  const rowsPerPage = 3; // Cambia esto para mostrar más o menos filas por página

  const handleNext = () => {
    if ((page + 1) * rowsPerPage < data.length) {
      setPage(page + 1);
    }
  };

  const handlePrevious = () => {
    if (page > 0) {
      setPage(page - 1);
    }
  };

  const handleSelect = (index) => {
    // Lógica para manejar la selección de la fila
    console.log(`Selected: ${resumeData[index].balance}`);
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
                    <TableCell sx={{ color: '#fff', fontWeight: 'bold' }}>First Name</TableCell>
                    <TableCell sx={{ color: '#fff', fontWeight: 'bold' }}>Last Name</TableCell>
                    <TableCell sx={{ color: '#fff', fontWeight: 'bold' }}>UID</TableCell>
                    <TableCell sx={{ color: '#fff', fontWeight: 'bold' }}>Model</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {data.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage).map((row, index) => (
                    <TableRow key={index} sx={{ '&:hover': { backgroundColor: '#e3f2fd' } }}>
                      <TableCell>{row.firstName}</TableCell>
                      <TableCell>{row.lastName}</TableCell>
                      <TableCell>{row.uid}</TableCell>
                      <TableCell>{row.model}</TableCell>
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
        <Button variant="contained" onClick={handleNext} disabled={(page + 1) * rowsPerPage >= data.length} sx={{ ml: 2 }}>
          Next
        </Button>
      </Grid>

      {/* Sección Resume */}
      <Grid item xs={12} sx={{ mt: 4 }}>
        <Typography variant="h5" align="center" gutterBottom sx={{ backgroundColor: '#4caf50', color: '#fff', padding: 2, borderRadius: 1 }}>
          Resume
        </Typography>
        <Animate type="fade">
          <MPaper>
            <TableContainer component={Paper} sx={{ boxShadow: 3, borderRadius: 2 }}>
              <Table>
                <TableHead sx={{ backgroundColor: '#4caf50', color: '#fff' }}>
                  <TableRow>
                    <TableCell sx={{ color: '#fff', fontWeight: 'bold' }}>Balance</TableCell>
                    <TableCell sx={{ color: '#fff', fontWeight: 'bold' }}>Status</TableCell>
                    <TableCell sx={{ color: '#fff', fontWeight: 'bold' }}>User Type</TableCell>
                    <TableCell sx={{ color: '#fff', fontWeight: 'bold' }}>Select</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {resumeData.map((resume, index) => (
                    <TableRow key={index} sx={{ '&:hover': { backgroundColor: '#c8e6c9' } }}>
                      <TableCell>{resume.balance}</TableCell>
                      <TableCell>{resume.status}</TableCell>
                      <TableCell>{resume.userType}</TableCell>
                      <TableCell>
                        <Button variant="contained" onClick={() => handleSelect(index)} sx={{ backgroundColor: '#f57c00', '&:hover': { backgroundColor: '#ef6c00' } }}>
                          Select
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
    </Grid>
  );
};

export default InfoPage;
