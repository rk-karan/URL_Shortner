import { createContext } from "react";
const SnackBarContext = createContext({
    setMessage: "",
    setSeverity: "",
    displaySnackBar: ""
});
export default SnackBarContext;