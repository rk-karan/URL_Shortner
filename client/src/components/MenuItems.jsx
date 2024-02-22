import React , {useContext} from 'react';
import MenuItem from '@mui/material/MenuItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import DeleteIcon from '@mui/icons-material/Delete';
import Settings from '@mui/icons-material/Settings';
import Logout from '@mui/icons-material/Logout';
import { useNavigate } from 'react-router-dom';
import { logoutUser } from '../utils/api';
import { removeUser } from  "../redux/userSlice";
import { useDispatch } from 'react-redux';
import SnackBarContext from '../utils/snackBarContext';

export const MenuItems = ({handleModalOpen}) => {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const {setShowSnackbar , setMessage, setSeverity } = useContext(SnackBarContext);

  const handleLogout = async () => {
    try {
        await logoutUser();
        dispatch(removeUser());
        navigate('/login');
        setMessage("Logged out successfully!");
        setSeverity("success");
        setShowSnackbar(true);
    } catch (err) {
        console.error("Error logging out:", err);
        setMessage(err.response.data.detail);
        setSeverity("success");
        setShowSnackbar(true);
    }
};

  const handleChangePassword = async () => {
    navigate('/changePassword');
  };

  const handleDeleteAccount = ()=> {
    console.log("Delete Account");
    handleModalOpen();
  }

  return (
    <>
      <MenuItem onClick={handleDeleteAccount}>
          <ListItemIcon>
            <DeleteIcon fontSize="small" />
          </ListItemIcon>
          Delete account
        </MenuItem>
        <MenuItem onClick={handleChangePassword}>
          <ListItemIcon>
            <Settings fontSize="small" />
          </ListItemIcon>
          Change Password
        </MenuItem>
        <MenuItem onClick={handleLogout}>
          <ListItemIcon>
            <Logout fontSize="small" />
          </ListItemIcon>
          Logout
        </MenuItem>
    </>
  )
}

export default MenuItems