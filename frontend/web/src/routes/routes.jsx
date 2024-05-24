import React, {useContext} from 'react';
import {Route, Routes} from "react-router-dom";
import {Context} from "../index";
import PrivateRoute from "./PrivateRoute";
import AuthPage from "../pages/AuthPage/AuthPage";
import HomePage from "../pages/HomePage";

export const useRoutes = () => {
  const {store} = useContext(Context)

  return (
    <Routes>
      <Route
        path="/"
        element={store.isAuth ? <HomePage /> : <AuthPage />}
      />
      <Route path="/home" element={<PrivateRoute />}>
        <Route index element={<HomePage />} />
      </Route>
    </Routes>
  );
};

export default useRoutes;