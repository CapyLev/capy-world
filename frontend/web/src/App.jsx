import React, {useContext, useEffect} from 'react';
import {observer} from "mobx-react-lite";
import useRoutes from "./routes/routes";
import {Context} from "./index";

const App = () => {
  const routes = useRoutes();
  const {store} = useContext(Context)

   useEffect(() => {
      store.checkAuth()
  }, [store]);

  return <>{routes}</>;
}

export default observer(App);
