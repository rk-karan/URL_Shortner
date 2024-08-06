import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import { useNavigate } from 'react-router-dom';
import "./Header.css";
const  Header = () => {
    const navigate = useNavigate();
    const handleClick = (e) =>{
        e.preventDefault();
        console.log("Hello from Login!");
        navigate('/login');
    }
  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }} onClick={()=> navigate('/')} className = 'heading'>
            URL SHORTENER
          </Typography>
          <Button color="inherit" onClick={handleClick}>Sign in</Button>
        </Toolbar>
      </AppBar>
    </Box>
  );
}

export default Header;