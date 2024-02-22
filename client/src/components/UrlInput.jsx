import React, { useRef , useContext } from 'react';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import './UrlInput.css';
import { checkValidUrl } from "../utils/validate";
import {createShortUrl, getUser} from "../utils/api";
import {useDispatch } from 'react-redux';
import { addUser } from '../redux/userSlice';
import SnackBarContext from '../utils/snackBarContext';


const UrlInput = () => {
  const urlRef = useRef(null);
  const dispatch = useDispatch();
  const {setShowSnackbar , setMessage, setSeverity } = useContext(SnackBarContext);
  const handleSubmitUrl = async (e) => {
    e.preventDefault();
    const err = checkValidUrl(urlRef.current.value);
    if(err){
      setMessage(err);
      setSeverity("error");
      setShowSnackbar(true);
    }else{
      try{
          const res = await createShortUrl({"long_url" : urlRef.current.value});
          console.log(res);
          if(res.status === 201){
            console.log("Here");
            const userRes = await getUser();
            if(userRes.status === 200){
              dispatch(addUser(userRes.data));
            }
            urlRef.current.value = '';
            setMessage("URL added successfully!")
            setSeverity("success");
            setShowSnackbar(true);
          }
        }
      catch(err){
        console.log(err.response.data.detail);
        setMessage(err.response.data.detail);
        setSeverity("error");
        setShowSnackbar(true);
      }
    }
  }

  return (
    <div className='url-body-container'>
    <div className='div-info-para'>
      <p className='info-para'>Please provide URL to be shortened:</p>
    </div>
    <div className = 'form-data'>
        <Box
            component="form"
            sx={{
                '& .MuiTextField-root': { m : 1, width: "70%" },
            }}
        >
            <div>
                <TextField id="filled-basic" label = "URL" type = "input" variant="outlined" placeholder="Enter URL to be shortened" inputRef = {urlRef}/>
                <Button variant="contained" size = "large" type="submit" sx = {{m : 1 , height: '6.5ch'}} onClick={ (e) => handleSubmitUrl(e)} > Submit </Button>
            </div>
       </Box>
    </div>
  </div>
  )
}

export default UrlInput;