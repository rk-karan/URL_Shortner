import React, { useState, useRef } from 'react';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import './Login.css';
import  checkValidate from '../utils/validate';
import { loginUser, getUser, createUser } from '../utils/api';
import { useNavigate } from 'react-router-dom';
import { addUser } from '../redux/userSlice';
import { useDispatch } from 'react-redux';

const Login = () => {
    const [isSignIn, setIsSignIn] = useState(true);
    const [errorMessage, setErrorMessage] = useState(null);
    const nameRef = useRef('');
    const emailRef = useRef('');
    const passwordRef = useRef('');
    const navigate = useNavigate();
    const dispatch = useDispatch();

    const toggleSignInForm = () => {
        setIsSignIn(!isSignIn);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const err = checkValidate(emailRef.current.value, passwordRef.current.value);
        setErrorMessage(err);
        if (err) return;

        try {
            let rc = 200;
            if (!isSignIn) {
                const res = await createUser({ "name": nameRef.current.value, "email": emailRef.current.value, "password": passwordRef.current.value });
                rc = res.status;
            }

            if (rc === 200) {
                const formData = new FormData();
                formData.append('username', emailRef.current.value);
                formData.append('password', passwordRef.current.value);
                const res = await loginUser(formData);

                if (res.status === 200) {
                    const user = await getUser();
                    dispatch(addUser(JSON.parse(user.data)));
                    emailRef.current.value = '';
                    passwordRef.current.value = '';
                    navigate('/');
                } else {
                    console.log('Login failed');
                }
            } else {
                console.log('User creation failed');
            }
        } catch (err) {
            console.error('Error:', err);
        }
    };

    return (
        <Box
            component="form"
            sx={{
                '& .MuiTextField-root': { m: 2, width: '50ch' },
                display: 'flex',
                justifyContent: 'center',
                flexDirection: 'column'
            }}
            autoComplete="off"
            className='box'
            onSubmit={(e) => handleSubmit(e)}
        >
            {!isSignIn && (<TextField id="outlined-basic" label="Name" variant="outlined" inputRef={nameRef} type="input" required />)}
            <TextField id="outlined-basic" label="Email" variant="outlined" inputRef={emailRef} type="input" required />
            <TextField id="filled-basic" label="Password" type="password" variant="outlined" inputRef={passwordRef} required />
            <Button variant="contained" size="medium" style={{ width: '65ch' }} type="submit">
                {isSignIn ? `Login` : 'Signup'}
            </Button>
            <p className='para' onClick={toggleSignInForm}>{isSignIn ? `New User? Signup` : 'Already a user? Signin'}</p>
            <p className='para'>{errorMessage}</p>
        </Box>
    );
};

export default Login;
