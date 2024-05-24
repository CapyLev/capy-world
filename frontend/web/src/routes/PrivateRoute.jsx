import React from 'react';
import { Navigate, Outlet, useLocation } from "react-router-dom";
import {Context} from "../index";
import {useContext} from "react";
import NavBar from "../components/NavBar/NavBar";

const PrivateRoute = () => {
  const {store} = useContext(Context)
  const location = useLocation();

  return store.isAuth === true ? (
    <>
      <NavBar/>
      <Outlet />
    </>
  ) : (
    <>
      <Navigate to="/" state={{ from: location }} replace />
    </>
  );
};

export default PrivateRoute;