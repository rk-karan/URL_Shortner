import { loginUser, getUser,  createUser} from '../utils/api';

export const userLogin = async (formData)=>{
    try{
        const res = await loginUser(formData);
        if(res.status === 200){
            const user = await getUser();
            console.log(user.data);
            return [res.status , "User Created successfully!!"];
        }
    }
    catch(err){
        console.log(err);
        return [500 , `${err?.response?.data?.detail}`];
    }
}

export const userSignUp = async (formData) => {
    try{
        const res = await createUser(formData);
        console.log(res.status);
        return [res.status , "User created Successfully!"];
    }
    catch(err){
        console.log(err);
        return ([500 , `${err?.response?.data?.detail}`]);
    }
}