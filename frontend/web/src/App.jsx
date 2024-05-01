import React, {useContext, useEffect} from 'react';
import LoginForm from "./components/LoginForm";
import {Context} from "./index";
import {observer} from "mobx-react-lite";

const App = () => {
  const {store} = useContext(Context)

  useEffect(() => {
    if (localStorage.getItem("access")) {
      store.checkAuth()
    }
  }, [store]);


  if (store.isLoading) {
    return (
      <div>Loading...</div>
    )
  }

  return (
    <div>
      <h1>{store.isAuth ? `User in system. ${store.user.username}` : "U SHOULD LOGIN"}</h1>
      <LoginForm/>
    </div>
  )
}

export default observer(App);
