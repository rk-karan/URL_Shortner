import React from 'react';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import './Login.css';
import { useState } from 'react';

const Login = () => {
  const [isLogIn, setIsLogIn] = useState(true);
  return (
    <Box
      component = "form"
      sx={{
        '& .MuiTextField-root': {m:2, width: '50ch' },
        display: 'flex',
        justifyContent: 'center',
        flexDirection: 'column'
      }}
      autoComplete="off"
      className='box'
    >
      {!isLogIn && (<TextField id="outlined-basic" label="Name" variant="outlined" />)}
        <TextField id="outlined-basic" label="Email" variant="outlined" />
        <TextField id="filled-basic" label="Password" variant="outlined"/>
        <Button variant="contained" size="medium" style={ {width: '65ch'}}>
            { isLogIn ? `Login`: 'Signup'}
        </Button>
        <p className = 'para' onClick={() => setIsLogIn(!isLogIn)}>{ isLogIn ? `New User? Signup`: 'Already a user? Signin'}</p>
    </Box>
  )
}

export default Login