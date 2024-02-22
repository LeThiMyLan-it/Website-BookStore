import axiosHandle from "./AxiosHandle";
export const Login = (username, password) => {
    return axiosHandle.post(process.env.REACT_APP_URL_API + `Auth/Login?username=${username}&password=${password}`);
}