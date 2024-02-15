import React from 'react';
import { createBrowserRouter, Outlet, RouterProvider} from 'react-router-dom';
import Body from './BodyPage';
import Login from './Login';
import Header from '../components/Header';

const AppLayout = () => {
    return(
        <div>
            <Header/>
            <Outlet/>
        </div>
    )
}
const Books = () =>{
    return <p>Books</p>
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
                    path: "/books",
                    element: <Books></Books>
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