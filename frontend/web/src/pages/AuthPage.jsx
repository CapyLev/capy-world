import React, {useState} from 'react';
import LoginModal from "../components/AuthComponents/LoginModal/LoginModal";
import RegisterModal from "../components/AuthComponents/RegisterModal/RegisterModal";
import Button from "../components/Button/Button";

const AuthPage = () => {
  const [isLoginModalOpen, setLoginModalOpen] = useState(false);
  const [isRegisterModalOpen, setRegisterModalOpen] = useState(false);

  return (
    <div>
      <div>
        {/*<Logo class={style.logo} />*/}
        <h1>Capybara-World</h1>
      </div>
      <div>
        <div>
          <Button onClick={() => setLoginModalOpen(true)}>
            Sign In
          </Button>
          {isLoginModalOpen && (
            <LoginModal onClose={() => setLoginModalOpen(false)} />
          )}
        </div>
        <div>
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
