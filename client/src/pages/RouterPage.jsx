import React from 'react';
import { createBrowserRouter, Outlet, RouterProvider} from 'react-router-dom';
import Header from '../components/Header';
import Body from './BodyPage';
import Login from './Login';

const AppLayout = () => {
    return(
        <div>
            <Header/>
            <Outlet/>
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