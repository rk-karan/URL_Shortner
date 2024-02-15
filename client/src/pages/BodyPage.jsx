import * as React from 'react';
import {useSelector } from 'react-redux';
import { useEffect } from 'react';
import { useNavigate } from 'react-router';

const  Body = () => {
   const user = useSelector((store) => store.user);
   const navigate = useNavigate();
   useEffect(()=> {
      if(!user){
         navigate('/login');
      }
   }, [user]);
   return (
      <>
         <p>Body</p>
      </>
   )
}

export default Body;