import axios from "axios";

export const baseURL = "http://localhost:8000/"

const API = axios.create({
    baseURL: baseURL,
    withCredentials: true,
    credentials: 'include'
});

export const loginUser = (data) => {
    return API.post('/user/login', data);
};

export const getUser = () => {
    return API.get('/user/me');
};

export const createUser = (data) => {
    return API.post('/user/create_user', {...data});
};

export const logoutUser = () => {
    return API.post('/user/logout');
}

export const createShortUrl = (data)  =>{
    return API.post('/url/create_url', {...data})
}

export const redirectURL = (data) => {
    console.log(`${baseURL}${data}`);
    return API.get(`${baseURL}${data}`);
}

export const updateURL = (data) => {
    console.log(data);
    return API.put('/url/edit_url' , {...data});
}

export const deleteURL = (data) => {
    console.log(data);
    return API.put('/url/delete_url' , {...data});
}