import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { logoutAsync } from "../slices/authSlice";
import dashboardStyle from "./dashboard.module.css";
import { FormContainer } from "./FormContainer";
export const Dashboard = ({ setBackgroundColor }) => {
  const user = useSelector((state) => state.auth.user);
  const dispatch = useDispatch();
  const handleLogOut = (e) => {
    e.preventDefault();
    dispatch(logoutAsync());
  };

  if (!Object.keys(user).length) {
    return <FormContainer setBackgroundColor={setBackgroundColor} />;
  }

  return (
    <div className={dashboardStyle["dashboard-container"]}>
      <h2 className={dashboardStyle["dashboard-header"]}>
        Session Based Authentication Using DRF and React
      </h2>
      <h1 className={dashboardStyle["dashboard-welcome"]}>
        {" "}
        Hello and welcome, {user.username}!. We're thrilled to have you here
      </h1>
      <div className="col text-center">
        <button
          className="btn btn-outline-light "
          onClick={(e) => handleLogOut(e)}
        >
          Logout
        </button>
      </div>
    </div>
  );
};
