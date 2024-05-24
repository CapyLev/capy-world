import React, {useState} from 'react';
import LoginModal from "../../components/AuthComponents/LoginModal/LoginModal";
import RegisterModal from "../../components/AuthComponents/RegisterModal/RegisterModal";
import Button from "../../components/Button/Button";
import styles from "./AuthPage.module.css";


const AuthPage = () => {
  const [isLoginModalOpen, setLoginModalOpen] = useState(false);
  const [isRegisterModalOpen, setRegisterModalOpen] = useState(false);

  return (
    <div className={styles.container}>
      <div className={styles.title}>
        {/*<Logo class={style.logo} />*/}
        <h1>Capybara-World</h1>
      </div>
      <div className={styles.buttonContainer}>
        <div className={styles.buttonItem}>
          <Button onClick={() => setLoginModalOpen(true)}>
            Sign In
          </Button>
          {isLoginModalOpen && (
            <LoginModal onClose={() => setLoginModalOpen(false)} />
          )}
        </div>
        <div className={styles.buttonItem}>
          <Button onClick={() => setRegisterModalOpen(true)}>
            Sign Up
          </Button>
          {isRegisterModalOpen && (
            <RegisterModal onClose={() => setRegisterModalOpen(false)} />
          )}
        </div>
      </div>
    </div>
  );
};

export default AuthPage;
