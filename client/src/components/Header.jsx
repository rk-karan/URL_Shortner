import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';

import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Menu from '@mui/material/Menu';

import MenuItems from './MenuItems';
import ToolBarContent from './ToolBarContent';
import DeleteUserModal from './DeleteUserModal';

import { getUser } from '../utils/api';
import { addUser } from  "../redux/userSlice";

import "./Header.css";
import {paperProps} from "./menuStyle";

const Header = () => {
    const navigate = useNavigate();
    const user = useSelector((store) => store.user);
    const dispatch = useDispatch();
    const [anchorEl, setAnchorEl] = useState(null);
    const open = Boolean(anchorEl);
    const [showModal , setShowModal] = useState(false);
    const handleModalOpen = () => setShowModal(true);
    const handleModalClose = () => setShowModal(false);

    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
    };
    const handleClose = () => {
        setAnchorEl(null);
    };


    useEffect(() => {
        const fetchUser = async () => {
            try {
                const res = await getUser();
                if (res.status === 200 && !user) {
                    dispatch(addUser(res.data));
                    // navigate('/');
                }
            } catch (err) {
                console.error("Error checking user status:", err);
            }
        };

        fetchUser();
    }, [user, dispatch, navigate]);

    return (
    <>
        <Box sx={{ flexGrow: 1 }}>
            <AppBar position="static">
                <ToolBarContent handleClick={handleClick} open = {open} /> {/*   If user, then Profile Actions else Login*/}
            </AppBar>
        </Box>
        <Menu
            anchorEl={anchorEl}
            id="account-menu"
            open={open}
            onClose = {handleClose}
            onClick = {handleClose}
            PaperProps = { paperProps }
            transformOrigin={{ horizontal: 'right', vertical: 'top' }}
            anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
        >
            <MenuItems handleModalOpen = {handleModalOpen}/>  {/*   If user, then Settings */}

        </Menu>
        <DeleteUserModal showModal = {showModal} handleModalClose={handleModalClose}/>
    </>

    );
};

export default Header;
