import React, {useContext, useState} from 'react';
import {Context} from "../index";
import {observer} from "mobx-react-lite";

const RegisterForm = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const {store} = useContext(Context)

  return (<div>
    <input onChange={e => setUsername(e.target.value)} type="text" placeholder="Username"/>
    <input onChange={e => setEmail(e.target.value)} type="email" placeholder="Email"/>
    <input onChange={e => setPassword(e.target.value)} type="password" placeholder="Password"/>
    <button onClick={() => store.register(username, email, password)}>Register</button>
  </div>);

};

export default observer(RegisterForm);
