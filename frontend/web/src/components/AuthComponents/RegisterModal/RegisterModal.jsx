import React, {useContext, useState} from 'react';
import {observer} from "mobx-react-lite";
import {Context} from "../../../index";
import style from "../AuthComponents.module.css"
import {useNavigate} from "react-router-dom";
import Button from "../../Button/Button";


const RegisterModal = (props) => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();
  const {store} = useContext(Context)
  const {onClose} = props;

  const handleModalClick = (e) => {
    e.stopPropagation();
  };

  const handleSubmit = () => {
    if (username && password && email) {
      store.register(username, email, password).then(() => {
        if (store.isAuth) {
          navigate(`/home`);
          onClose();
        } else {
          console.error('Try again later');
        }
      })
    }
  }

  return (
    <div className={style.modalBackground} onClick={onClose}>
      <div className={style.modal} onClick={handleModalClick}>
        <div className={style.inputContainer}>
          <input
            type="text"
            placeholder="Username"
            value={username}
            onInput={(e) => setUsername(e.target.value)}
          />
        </div>

        <div className={style.inputContainer}>
          <input
            type="email"
            placeholder="Email"
            value={email}
            onInput={(e) => setEmail(e.target.value)}
          />
        </div>

        <div className={style.inputContainer}>
          <input
            type="password"
            placeholder="Password"
            value={password}
            onInput={(e) => setPassword(e.target.value)}
          />
        </div>

        <Button className={style.acceptButton} onClick={handleSubmit}>
          Login
        </Button>
      </div>
    </div>
  );
};


export default observer(RegisterModal);
