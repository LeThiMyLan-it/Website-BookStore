import axios from "axios";

const instance = axios.create(
    {
        baseURL: process.env.REACT_APP_URL_API,
        timeout: 300000
    }
);
instance.interceptors.request.use(
    (config) => {
        config.headers["Content-Type"] = "application/json";
        return config;
    },
    error => {
        Promise.reject(error);
    }
);
instance.interceptors.response.use(
    (response) => {
        return response.data
    },
    (error) => {
        return error.response
    }
);
export default instance;


    // instance.interceptors.request.use(
    //     (config) => {
    //         config.headers.Authorization = `Bearer ${sessionStorage.getItem('token')}`;
    //         return config;
    //     },
    //     error => {
    //         Promise.reject(error);
    //     }
    // );