import React from 'react';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import Tooltip from '@mui/material/Tooltip';
import Avatar from '@mui/material/Avatar';
import IconButton from '@mui/material/IconButton';

import { useNavigate } from 'react-router-dom';
import { useSelector} from 'react-redux';

const ToolBarContent = ({ open , handleClick}) => {
    const navigate = useNavigate();
    const user = useSelector((store) => store.user);

    const handleSignIn = () => {
        navigate('/login');
    };

    const handleLogoClick = () => {
        navigate('/');
    };
  return (
    <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }} onClick = {handleLogoClick} className="header-title">
                        URL SHORTENER
        </Typography>
        {
            !user ?
            <Button color="inherit" onClick={handleSignIn}>Sign in</Button>
            :
            <Tooltip title="Account settings">
                <IconButton
                    onClick={handleClick}
                    size = "medium"
                    sx = {{ ml: 2 }}
                    aria-controls={open ? 'account-menu' : undefined}
                    aria-haspopup="true"
                    aria-expanded={open ? 'true' : undefined}
                >
                    <Avatar sx={{ width: 32, height: 32 }}>{user.user.name[0]}</Avatar>
                </IconButton>
            </Tooltip>
        }
    </Toolbar>
  )
}

export default ToolBarContent