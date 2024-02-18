import * as React from 'react';
import {useSelector } from 'react-redux';
import { useEffect } from 'react';
import { useNavigate } from 'react-router';
import UrlInput from '../components/UrlInput';
import DisplayUrlMapping from '../components/DisplayUrlMapping';
import './body.css'

const  Body = () => {
   const user = useSelector((store) => store.user);
   const navigate = useNavigate();
   useEffect(()=> {
      if(!user){
         navigate('/login');
      }
   }, [user]);
   return (
    <div className='body-container'>
      <UrlInput/>
      <DisplayUrlMapping/>
    </div>
   )
}

export default Body;