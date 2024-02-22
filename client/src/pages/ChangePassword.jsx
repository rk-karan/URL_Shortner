import React from 'react';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import "./ChangePassword.css";
import { useRef , useContext } from 'react';
import checkValidate from '../utils/validate';
import { useDispatch, useSelector } from 'react-redux';
import { changeCurrentPassword } from '../utils/api';
import {useNavigate} from "react-router-dom";
import { removeUser } from '../redux/userSlice';
import SnackBarContext from '../utils/snackBarContext';

const ChangePassword = () => {
    const oldPasswordRef = useRef(null);
    const newPasswordRef = useRef(null);
    const confirmNewPasswordRef = useRef(null);
    const navigate = useNavigate();
    const dispatch = useDispatch();
    const {setShowSnackbar , setMessage, setSeverity } = useContext(SnackBarContext);
    const user = useSelector((state) => state.user);
    if(!user){
        return <>Loading....</>;
    }

    const handleChangePassword = async (e) => {
        e.preventDefault();
        const err = checkValidate(user.user.email , newPasswordRef.current.value);
        if(err){
            console.log(err);
            setMessage("Entered Password is not valid");
            setSeverity("error");
            setShowSnackbar(true);
            return;
        }else{
            if(oldPasswordRef.current.value === newPasswordRef.current.value){
                console.log("Same password!");
                setMessage("Same passwords!");
                setSeverity("error");
                setShowSnackbar(true);
                return;
            }else if(newPasswordRef.current.value !== confirmNewPasswordRef.current.value){
                setMessage("Entered passwords do not match!");
                setSeverity("error");
                setShowSnackbar(true);
                return;
            }
            try{
                const res = await changeCurrentPassword({"new_password" : newPasswordRef.current.value , "old_password" : oldPasswordRef.current.value});
                if(res.status === 200){
                    console.log("Password changed!");
                    dispatch(removeUser());
                    navigate('/');
                    setMessage("Password Changed successfully!");
                    setSeverity("success");
                    setShowSnackbar(true);
                }else{
                    setMessage("Some error occurred!");
                    setSeverity("error");
                    setShowSnackbar(true);
                }
            }
            catch(err){
                setMessage(err.response.data.detail);
                setSeverity("error");
                setShowSnackbar(true);
            }
        }
    }

    return (
    <div className ='formData'>
        <Box
            component="form"
            sx={{
                '& .MuiTextField-root': { m : 1, width: "50%" },
            }}
            onSubmit = {(e) => e.preventDefault()}
        >
            <div>
                    <TextField key = "key-old-password" id="filled-basic id1" label="Old Password" type="password" variant="outlined" required inputRef = {oldPasswordRef}/>
            </div>
            <div>
                    <TextField key = "key-new-password" id="filled-basic id2" label="New Password" type="password" variant="outlined" required inputRef={newPasswordRef}/>
            </div>
            <div>
                    <TextField key = "key-new-password" id="filled-basic id3" label="Confirm New Password" type="password" variant="outlined" required inputRef={confirmNewPasswordRef}/>
            </div>
            <div>
                    <Button variant="contained" size="medium" type="submit" sx = {{ width: '50%', marginLeft : 1 }} onClick = {handleChangePassword}> Submit </Button>
            </div>
        </Box>
    </div>
  );
};

export default ChangePassword;