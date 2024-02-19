import React from 'react';
import {useSelector } from 'react-redux';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';
import './DisplayTable.css';
import {baseURL , redirectURL} from "../utils/api";

const DisplayUrlMapping = () => {
    const user = useSelector(store => store.user);
    if(!user){
        return;
    }
    const handleClickShortUrl = async(e, short_url) => {
        e.preventDefault();
        try {
            const response = await fetch(`http://localhost:8000/${short_url}`);
            if (response.ok) {
              // If response status is in the 300 range, it's a redirect
              if (response.status >= 300 && response.status < 400) {
                const redirectUrl = response.headers.get('Location');
                if (redirectUrl) {
                  window.location.href = redirectUrl; // Redirect the user to the new URL
                }
              }
              // Handle other responses if needed
            } else {
              throw new Error('Failed to fetch data');
            }
          } catch (error) {
            console.error('Error fetching data:', error);
          }
    }
  return (
    <div>
        <div className = 'table-info'>
            <p className ='table-info-para'> List of URLs shortened by {user?.user?.name}</p>
        </div>
        <div>
            <TableContainer component={Paper} >
            <Table>
                <TableHead>
                <TableRow>
                    <TableCell>Index</TableCell>
                    <TableCell>URL</TableCell>
                    <TableCell>Mapping</TableCell>
                </TableRow>
                </TableHead>
                <TableBody>
                {user?.urls?.map((url , index) => (
                    <TableRow key={url.id}>
                    <TableCell>{index + 1}</TableCell>
                    <TableCell>{url.long_url}</TableCell>
                    <TableCell 
                    sx = {{
                        cursor: 'pointer'
                    }}
                    onClick={(e)=> handleClickShortUrl(e, url.short_url)}
                    >{`${baseURL}${url.short_url}`}</TableCell>
                    </TableRow>
                ))}
                </TableBody>
            </Table>
            </TableContainer>
        </div>
    </div>
  );
};

export default DisplayUrlMapping;
