import React from 'react';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import './Login.css';
import { useState, useRef } from 'react';
import checkValidate from "../utils/validate";

import { loginUser } from '../utils/api';
import axios from 'axios';

const userLogin = async (formData)=>{
  const res = await loginUser(formData);
  console.log(res);
}

const Login = () => {
  const [isSignIn, setIsSignIn] = useState(true);
  const name = useRef();
  const email = useRef();
  const password = useRef();

  const toggleSignInForm = () => {
    setIsSignIn(!isSignIn);
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    const errorMessage = checkValidate(email.current.value, password.current.value);
    console.log(errorMessage);
    if (errorMessage) {
      console.log(errorMessage);
      return;
    }
    const formData = new FormData();
    formData.append('username' , email.current.value);
    formData.append('password' , password.current.value);
    console.log(formData);
    userLogin(formData);
  }

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
      onSubmit = {(e) => handleSubmit(e)}
    >
      {!isSignIn && (<TextField id="outlined-basic" label="Name" variant="outlined" inputRef = {name} type = "input"/>)}
        <TextField id="outlined-basic" label="Email" variant="outlined"  inputRef = {email} type = "input"/>
        <TextField id="filled-basic" label="Password" type = "password" variant="outlined" inputRef = {password}/>
        <Button variant="contained" size="medium" style={ {width: '65ch'}} type = "submit" >
            { isSignIn ? `Login`: 'Signup'}
        </Button>
        <p className = 'para' onClick={toggleSignInForm}>{ isSignIn ? `New User? Signup`: 'Already a user? Signin'}</p>
    </Box>
  )
}

export default Login