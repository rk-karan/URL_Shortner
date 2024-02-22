import React from 'react';
import {useSelector } from 'react-redux';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';
import './DisplayTable.css';
import {clientURL} from "../utils/api";
import UpdateModal from './UpdateModal';
import DeleteModal from './DeleteModal';

const DisplayUrlMapping = () => {
    const user = useSelector(store => store.user);
    if(!user){
        return;
    }
    const handleClickShortUrl = async(e, short_url) => {
        e.preventDefault();
        window.location.href = `${clientURL}${short_url}`
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
                    <TableCell align="center">Index</TableCell>
                    <TableCell align="center">URL</TableCell>
                    <TableCell align="center">Mapping</TableCell>
                    <TableCell align="center">Actions</TableCell>
                </TableRow>
                </TableHead>
                <TableBody>
                {user?.urls?.map((url , index) => (
                    <TableRow key={url.id}>
                    <TableCell align="center">{index + 1}</TableCell>
                    <TableCell align="center">{url.long_url}</TableCell>
                    <TableCell 
                    sx = {{
                        cursor: 'pointer',
                    }}
                    align="center"
                    onClick={(e)=> handleClickShortUrl(e, url.short_url)}
                    >{`${clientURL}${url.short_url}`}</TableCell>
                    <TableCell align="center"><span className='update-btn'><UpdateModal url = {url}/></span><span className='delete-button'><DeleteModal url = {url}/></span></TableCell>
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
