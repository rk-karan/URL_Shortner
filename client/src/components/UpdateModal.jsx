import {useState, useRef} from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import FormControl from '@mui/material/FormControl';
import Modal from '@mui/material/Modal';
import InputLabel from '@mui/material/InputLabel';
import OutlinedInput from '@mui/material/OutlinedInput';
import {checkValidUrl} from "../utils/validate";
import { updateURL, getUser } from '../utils/api';
import {useDispatch } from 'react-redux';
import { addUser } from '../redux/userSlice';
import Typography from '@mui/material/Typography';

const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 800,
  bgcolor: 'background.paper',
  border: '2px solid #000',
  boxShadow: 24,
  p: 4,
  m: 2
};

export const UpdateModal = ({url}) => {
    const [open, setOpen] = useState(false);
    const [errMessage , setErrMessage] = useState("");
    const dispatch = useDispatch();
    const handleOpen = () => setOpen(true);
    const handleClose = () => {
        setErrMessage("");
        setOpen(false);
    }

    const newURLRef = useRef(null);

    const handleUpdateUrl = async(e) =>{
        e.preventDefault();
        const err = checkValidUrl(newURLRef.current.value);
        if(err){
            console.log(err);
            setErrMessage(err);
            return;
        }
        if(newURLRef.current.value === url.long_url){
            console.log("Same url");
            setErrMessage("Same URL, Change to update")
            return;
        }else{
            try{
                const res = await updateURL({"new_long_url": newURLRef.current.value , "old_long_url": url.long_url , "id": url.id});
                console.log(res);
                if(res.status === 200){
                    const userReq = await getUser();
                    if(userReq.status === 200){
                        setErrMessage("");
                        dispatch(addUser(userReq.data));
                        handleClose();
                    }
                }
            }catch(err){
                console.log(err);
            }
        }

    }

    return (
    <div>
        <Button onClick={handleOpen}>Update</Button>
        <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
        >
        <Box sx={style}>
        <Typography variant="p" component="p" color = "error" sx = {{marginLeft: '35%'}}>{errMessage}</Typography>
        <br/>
        <FormControl fullWidth sx={{ m: 1}}>
          <InputLabel htmlFor="outlined-adornment-amount">New URL</InputLabel>
          <OutlinedInput
            id="outlined-adornment-amount"
            label="New URL"
            defaultValue={url.long_url}
            inputRef = {newURLRef}
          />
          <Button variant="outlined" sx = {{ marginLeft: '35%', marginTop: '2%', width: '150px'}} type = 'submit' onClick={(e) => handleUpdateUrl(e)}>Update</Button>
        </FormControl>
        </Box>
        </Modal>
    </div>
  );
}

export default UpdateModal;