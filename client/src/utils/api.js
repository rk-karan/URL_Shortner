import axios from "axios";

const API = axios.create({
    baseURL: 'http://localhost:8000/',
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