import React from 'react';
import { Navigate, Outlet, useLocation } from "react-router-dom";
import {Context} from "../index";
import {useContext} from "react";

const PrivateRoute = () => {
  const {store} = useContext(Context)
  const location = useLocation();
  console.log(store.isAuth);
  return store.isAuth === true ? (
    <>
      <Outlet />
    </>
  ) : (
    <Navigate to="/" state={{ from: location }} replace />
  );
};

export default PrivateRoute;