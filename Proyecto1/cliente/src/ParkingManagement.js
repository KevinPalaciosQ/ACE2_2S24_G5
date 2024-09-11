import React from "react";
import { DataGrid } from '@mui/x-data-grid';

const columns = [
  { field: 'name', headerName: 'Name', width: 200 },
  { field: 'age', headerName: 'Age', width: 100 },
  { field: 'nickname', headerName: 'Nickname', width: 150 },
  { field: 'employee', headerName: 'Employee', width: 130, type: 'boolean' }
];

const rows = [
  { id: 1, name: 'Giacomo Guilizzoni', age: 40, nickname: 'Peldi', employee: true },
  { id: 2, name: 'Marco Botton', age: 38, nickname: 'Potato', employee: true },
  { id: 3, name: 'Mariah Maclachlan', age: 41, nickname: 'Val', employee: false },
  { id: 4, name: 'Valerie Liberty', age: 35, nickname: 'Val', employee: true }
];

const ParkingManagement = () => {
  return (
    <div style={{ height: 400, width: '100%' }}>
      <h2>Administración de Parqueos</h2>
      <p>Parqueos disponibles.</p>
      <DataGrid rows={rows} columns={columns} pageSize={5} checkboxSelection />
    </div>
  );
};

export default ParkingManagement;
