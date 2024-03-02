import React, { useState,useEffect } from "react";
import "./styles/index.css";
import Shape from "./components/Shape";
import { Toaster } from "react-hot-toast";
import { FormContainer } from "./components/FormContainer";
import { useSelector } from "react-redux";
import { Dashboard } from "./components/Dashboard";
import { checkAuthenticatedAsync } from "./slices/authSlice";
import { useDispatch } from "react-redux";
export const App = () => {

  const isAuthenticated = useSelector((state) => state.auth.isAuthenticated);
  const loading = useSelector((state) => state.auth.loading);
  const [backgroundColor, setBackgroundColor] = useState("#5B5EA6");
  const dispatch = useDispatch()

  const numberOfShapes = 20;

  const shapes = Array.from({ length: numberOfShapes }, (_, index) => (
    <Shape key={index} />
  ));

  useEffect(() => {
    dispatch(checkAuthenticatedAsync());

  }, []);


  if (isAuthenticated) {
    return (
      <div className="body" style={{ background: backgroundColor }}>
        <div className="shape-container">{shapes}</div>
        <Dashboard setBackgroundColor={setBackgroundColor} />
      </div>
    );
  }

  return (
    <>
      <div className="body" style={{ background: backgroundColor }}>
        <div className="shape-container">{shapes}</div>
        {!loading && (<FormContainer setBackgroundColor={setBackgroundColor} />)}
      </div>

      <Toaster
        position="bottom-right"
        toastOptions={{
          style: {
            borderRadius: '10px',
            background: '#333',
            color: '#fff',
          },
        }}
      />
    </>
  );
};

export default App;
