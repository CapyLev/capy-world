import React, {useContext, useState} from 'react';
import {observer} from "mobx-react-lite";
import {Context} from "../../../index";
import {useNavigate} from "react-router-dom";
import style from "../AuthComponents.module.css"
import Button from "../../Button/Button";

const LoginModal = (props) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();
  const {store} = useContext(Context)
  const {onClose} = props;

  const handleModalClick = (e) => {
    e.stopPropagation();
  };

  const handleSubmit = () => {
    if (username && password) {
      store.login(username, password).then(() => {
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

export default observer(LoginModal);
