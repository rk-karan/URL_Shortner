import React from 'react';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import './Login.css';
import { useState, useRef } from 'react';
import checkValidate from "../utils/validate";
import { loginUser, getUser,  createUser} from '../utils/api';
import { useNavigate } from 'react-router-dom';
import { addUser } from '../redux/userSlice';
import { useDispatch } from 'react-redux';
import Header from '../components/Header';


const Login = () => {
  const [isSignIn, setIsSignIn] = useState(true);
  const [errorMessage, setErrorMessage] = useState(null)
  const name = useRef();
  const email = useRef();
  const password = useRef();
  const navigate = useNavigate();
  const dispatch = useDispatch();


  const toggleSignInForm = () => {
    setIsSignIn(!isSignIn);
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    const err = checkValidate(email.current.value, password.current.value);
    setErrorMessage(err);
    if (err) {
      return;
    }
	const formData = new FormData();
	formData.append('username' , email.current.value);
	formData.append('password' , password.current.value);
	let rc = 200;
    if(!isSignIn){
      try{
        const res = await createUser({"name": name.current.value , "email" : email.current.value , "password": password.current.value});
        rc = res.status;
      }
      catch(err){
        rc = err?.response?.status;
        console.log(err);
      }
    }

	if(rc !==200){
		return;
	}
	try{
		const res = await loginUser(formData);
        if(res.status === 200){
			      rc = 200;
            const user = await getUser();
            dispatch(addUser(JSON.parse(user.data)));
        }
	}catch (err){
		rc = err?.response?.status;
		console.log(err);
	}
	if(rc !== 200){
		return;
	}
	email.current.value = null;
	password.current.value = null;
	navigate('/');
  }

  return (
    <>
      {/* <Header/> */}
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
        {!isSignIn && (<TextField id="outlined-basic" label="Name" variant="outlined" inputRef = {name} type = "input"  required />)}
          <TextField id="outlined-basic" label="Email" variant="outlined"  inputRef = {email} type = "input"  required />
          <TextField id="filled-basic" label="Password" type = "password" variant="outlined" inputRef = {password}  required/>
          <Button variant="contained" size="medium" style={ {width: '65ch'}} type = "submit" >
              { isSignIn ? `Login`: 'Signup'}
          </Button>
          <p className = 'para' onClick={toggleSignInForm}>{ isSignIn ? `New User? Signup`: 'Already a user? Signin'}</p>
      <p className = 'para' >{errorMessage}</p>
      </Box>
    </>
  )
}

export default Login