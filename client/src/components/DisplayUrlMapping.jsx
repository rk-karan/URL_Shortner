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
    const handleClickShortUrl = async(e, id) => {
        e.preventDefault();
        console.log(id);
        try{
            const res = await redirectURL(id);
            console.log(res);
        }
        catch(err){
            console.log(err);
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
                    onClick={(e)=> handleClickShortUrl(e, url.id)}
                    >{`${baseURL}${url.id}`}</TableCell>
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
