import axios from "axios";

export const baseURL = "http://localhost:8000/"
export const clientURL = "http://localhost:3000/"

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

export const updateURL = (data) => {
    console.log(data);
    return API.put('/url/edit_url' , {...data});
}

export const deleteURL = (data) => {
    console.log(data);
    return API.put('/url/delete_url' , {...data});
}

export const changeCurrentPassword = (data) => {
    return API.put('/user/change_password' , {...data});
}

export const deleteUser = () => {
    return API.delete('/user/delete_user');
}