import React, { useEffect } from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import { useNavigate } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import { getUser, logoutUser } from '../utils/api';
import { addUser, removeUser } from  "../redux/userSlice";
import "./Header.css";

const Header = () => {
    const navigate = useNavigate();
    const user = useSelector((store) => store.user);
    const dispatch = useDispatch();

    useEffect(() => {
        const fetchUser = async () => {
            try {
                const res = await getUser();
                if (res.status === 200 && !user) {
                    dispatch(addUser(JSON.parse(res.data)));
                    navigate('/');
                }
            } catch (err) {
                console.error("Error checking user status:", err);
            }
        };

        fetchUser();
    }, [user, dispatch, navigate]);

    const handleLogout = async () => {
        try {
            await logoutUser();
            dispatch(removeUser());
            navigate('/login');
        } catch (err) {
            console.error("Error logging out:", err);
        }
    };

    const handleSignIn = () => {
        navigate('/login');
    };

    const handleLogoClick = () => {
        navigate('/');
    };

    return (
        <Box sx={{ flexGrow: 1 }}>
            <AppBar position="static">
                <Toolbar>
                    <Typography variant="h6" component="div" sx={{ flexGrow: 1 }} onClick={handleLogoClick} className="header-title">
                        URL SHORTENER
                    </Typography>
                    {
                        !user ?
                        <Button color="inherit" onClick={handleSignIn}>Sign in</Button> :
                        <Button color="inherit" onClick={handleLogout}>Logout</Button>
                    }
                    <Button color="inherit" onClick={() => navigate('/books')}>Books</Button>
                </Toolbar>
            </AppBar>
        </Box>
    );
};

export default Header;
