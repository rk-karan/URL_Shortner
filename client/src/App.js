import Router from "./pages/RouterPage";
import appStore from "./redux/appStore";
import { Provider } from 'react-redux';

const App = ()=> {
  return (
    <Provider store = {appStore}>
      <Router/>
    </Provider>
  )
}
export default App;
