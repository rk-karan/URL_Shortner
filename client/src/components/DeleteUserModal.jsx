import React , {useContext} from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Modal from '@mui/material/Modal';
import { useDispatch } from 'react-redux';
import { deleteUser } from '../utils/api';
import { removeUser } from '../redux/userSlice';
import { useNavigate } from 'react-router-dom';
import SnackBarContext from '../utils/snackBarContext';


const modalStyle = {
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

const DeleteUserModal = ({showModal , handleModalClose}) => {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const {setShowSnackbar , setMessage, setSeverity } = useContext(SnackBarContext);

      const handleYes = async() => {
        try{
            const res = await deleteUser();
            if(res.status === 200){
                console.log("User deleted successfully");
                handleModalClose();
                dispatch(removeUser());
                navigate('/');
                setMessage("Deleted User Successfully!");
                setSeverity("success");
                setShowSnackbar(true);
            }
        }catch(err){
            setMessage("Some error occurred while deleting user!");
            setSeverity("error");
            setShowSnackbar(true);
        }
      }
      const handleNo = () => {
        handleModalClose();
      }

    return (
        <Modal
            open={showModal}
            onClose={handleModalClose}
            aria-labelledby="modal-modal-title"
            aria-describedby="modal-modal-description"
        >
            <Box sx={modalStyle}>
            <Typography id="modal-modal-title" variant="h6" component="h2">
                All data will be lost. Are you sure to delete account?
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

    )
}

export default DeleteUserModal