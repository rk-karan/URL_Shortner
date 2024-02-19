import React, { useRef } from 'react';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import SendIcon from '@mui/icons-material/Send';
import './UrlInput.css';
import { checkValidUrl } from "../utils/validate";
import {createShortUrl, getUser} from "../utils/api";
import {useDispatch } from 'react-redux';
import { addUser } from '../redux/userSlice';

const UrlInput = () => {

  const urlRef = useRef(null);
  const dispatch = useDispatch();
  const handleSubmitUrl = async (e) => {
    e.preventDefault();
    const err = checkValidUrl(urlRef.current.value);
    if(err){
      console.log(err);
    }else{
      const res = await createShortUrl({"long_url" : urlRef.current.value});
      console.log(res);
      if(res.status === 201){
        console.log("Here")
        const userRes = await getUser()
        if(userRes.status === 200){
          dispatch(addUser(userRes.data));
        }
        urlRef.current.value = '';
      }else{
        console.log("Some error occured!");
      }
    }
  }
  return (
    <div className='url-body-container'>
    <div className='div-info-para'>
      <p className='info-para'>Please provide URL to be shortened:</p>
    </div>
    <div className='div-submit-url'>
      <div className='div-input-url'>
        <TextField
          id="outlined"
          label="URL"
          placeholder="Enter URL to be shortened"
          sx={{
            width: '75ch',
            height: '7ch'
          }}
          inputRef = {urlRef}
        />
      </div>
      <div className='div-submit-button'>
        <Button
          variant="contained"
          endIcon={<SendIcon />}
          onClick={handleSubmitUrl}
          sx={{
            height: '7ch'
          }}
        >
          Shorten URL
        </Button>
      </div>
    </div>
  </div>
  )
}

export default UrlInput;