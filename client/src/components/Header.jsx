import React, { useEffect } from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import { useNavigate } from 'react-router-dom';
import {useSelector , useDispatch} from 'react-redux';
import { getUser , logoutUser } from '../utils/api';
import { addUser , removeUser } from  "../redux/userSlice";
import "./Header.css";

const  Header = () => {
    const navigate = useNavigate();
    const user = useSelector((store) => store.user);
    const dispatch = useDispatch();

    useEffect(() => {
      const helper = async () => {
        try{
          const res = await getUser();
          if(res.status === 200){
            if(!user){
              dispatch(addUser(JSON.parse(res.data)));
              navigate('/');
            }
          }
        }catch(err){
          if(user === null){
            navigate('/login');
          }
        }
      }
      helper();
    });

    const handleClick = (e) =>{
        e.preventDefault();
        navigate('/login');
    }
    const handleLogout = async() =>{
      try{
        const res = await logoutUser();
        console.log(res);
        dispatch(removeUser());
        navigate('/login');
      }catch(err){
        console.log(err);
      }
    }
    const handleLogoClick = (e) =>{
      e.preventDefault();
      navigate('/');
    }
  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }} onClick={(e) => handleLogoClick(e)} className = 'heading'>
            URL SHORTENER
          </Typography>
          {
            !user ? <Button color="inherit" onClick={handleClick}>Sign in</Button> : <Button color="inherit" onClick={handleLogout}>Logout</Button>
          }
          <Button color="inherit" onClick={() => navigate('/books')}>Books</Button>
        </Toolbar>
      </AppBar>
    </Box>
  );
}

export default Header;