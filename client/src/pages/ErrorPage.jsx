import React , {useState , useEffect} from 'react';
import {useParams } from 'react-router-dom';

const ErrorPage = () => {
    const [message , setErrorMessage] = useState("");
    const {id} = useParams();
    console.log(id);

    useEffect(()=> {
        fetch(`http://localhost:8000/${id}`, {method: 'GET', redirect: 'manual'}).then(response=> {
            if(response) {
                window.location.href = response.url
            }
        }).catch((err) => {
            console.log(err);
            setErrorMessage(err?.response?.data?.detail)
        })
    }, []);

    return (
        <div>{message}</div>
      )

}

export default ErrorPage