import axios from "axios";

const API = axios.create({
    baseURL: 'http://localhost:8000/',
    withCredentials: true,
    credentials: 'include'
});

export const loginUser = (data) => {
    return API.post('/user/login', data);
};