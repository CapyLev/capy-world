import React, {useContext, useState} from 'react';
import {Context} from "../index";
import {observer} from "mobx-react-lite";

const LoginForm = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const {store} = useContext(Context)

  return (<div>
    <input onChange={e => setUsername(e.target.value)} type="text" placeholder="Username"/>
    <input onChange={e => setPassword(e.target.value)} type="password" placeholder="Password"/>
    <button onClick={() => store.login(username, password)}>Login</button>
  </div>);
};

export default observer(LoginForm);
