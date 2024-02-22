import React, {useState} from 'react';
import { createBrowserRouter, Outlet, RouterProvider} from 'react-router-dom';
import Body from './BodyPage';
import Login from './Login';
import Header from '../components/Header';
import ChangePassword from './ChangePassword';
import Snackbar from '@mui/material/Snackbar';
import Alert from '@mui/material/Alert';
import SnackBarContext from "../utils/snackBarContext";
import ErrorPage from './ErrorPage';


const AppLayout = () => {
   const [message , setMessage ] = useState("");
   const [severity , setSeverity ] = useState("");
   const [showSnackbar , setShowSnackbar] = useState(false);
    return(
        <div>
            <SnackBarContext.Provider value = {{setMessage: setMessage , setSeverity: setSeverity , setShowSnackbar: setShowSnackbar}}>
                <Header/>
                <Outlet/>
            </SnackBarContext.Provider>
            <Snackbar open = {showSnackbar}  autoHideDuration={5000} onClose = {() => setShowSnackbar(false)} >
                <Alert
                    onClose = {() => setShowSnackbar(false)}
                    variant = "filled"
                    severity = {severity}
                    sx={{ width: '100%' }}
                >
                    {message}
                </Alert>
            </Snackbar>
        </div>
    )
}

const Router = () => {
    const appRouter = createBrowserRouter([
        {
            path: "/",
            element: <AppLayout></AppLayout>,
            children:[
                {
                    path: "/",
                    element: <Body></Body>
                },{
                    path: "/login",
                    element: <Login></Login>
                },
                {
                    path: "/changePassword",
                    element: <ChangePassword/>
                },{
                    path : "/:id",
                    element: <ErrorPage></ErrorPage>
                }
            ]
        }
    ]);
  return (
    <div>
        <RouterProvider router = {appRouter}/>
    </div>
  )
}

export default Router