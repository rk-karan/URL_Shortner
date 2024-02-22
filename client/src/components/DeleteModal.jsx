import {useState , useContext} from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Modal from '@mui/material/Modal';
import { deleteURL, getUser } from '../utils/api';
import { useDispatch } from 'react-redux';
import { addUser } from '../redux/userSlice';
import SnackBarContext from '../utils/snackBarContext';

const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 400,
  bgcolor: 'background.paper',
  border: '2px solid #000',
  boxShadow: 24,
  p: 4,
};

const DeleteModal = ({url})=> {
  const [open, setOpen] = useState(false);
  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);
  const dispatch = useDispatch();
  const {setShowSnackbar , setMessage, setSeverity } = useContext(SnackBarContext);


  const handleYes = async(e) => {
    e.preventDefault(e);
    try{
      const res = await deleteURL({"id": url.id , "long_url": url.long_url});
      if(res.status === 200){
        const userReq = await getUser();
        if(userReq.status === 200){
          dispatch(addUser(userReq.data));
          handleClose();
          console.log("deleted url")
          setMessage("Deleted URL successfully!");
          setSeverity("success");
          setShowSnackbar(true);
        }
      }
    }catch(err){
        setMessage("Some error occurred!");
        setSeverity("error");
        setShowSnackbar(true);
        console.log(err);
    }
  }
  const handleNo = (e) => {
    handleClose();
  }
  return (
    <div>
      <Button onClick={handleOpen}>Delete</Button>
      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box sx={style}>
          <Typography id="modal-modal-title" variant="h6" component="h2">
            Are you sure to delete?
          </Typography>
          <Box sx = {{
            display: 'flex',
            justifyContent: 'left',
            flexDirection: 'row'
          }}>
            <Button sx = {{marginLeft:1 , marginTop: 3}} variant="outlined" style = {{width: '300px'}} onClick = { (e) => handleYes(e)}>Yes</Button>
            <Button sx = {{marginLeft:30, marginTop: 3}} variant="outlined" style = {{width: '300px'}} onClick={handleNo}>No</Button>
          </Box>
        </Box>
      </Modal>
    </div>
  );
};

export default DeleteModal;