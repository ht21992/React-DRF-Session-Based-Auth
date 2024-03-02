import axios from "axios";
import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import Cookies from "js-cookie";
import toast from "react-hot-toast";

const initialState = {
  isAuthenticated: false,
  loading: true,
  user: {},
};

// Async action to handle login

export const loginAsync = (email, password) => async (dispatch) => {
  const config = {
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-CSRFToken": Cookies.get("csrftoken"),
    },
  };

  const body = JSON.stringify({ email, password });

  try {
    const res = await axios.post("/api/login/", body, config);

    if (res.status === 200) {
      dispatch(login(res.data));
    }
  } catch (error) {
    toast.error(error.response.data.error);
  }
};

export const logoutAsync = () => async (dispatch) => {
  const config = {
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-CSRFToken": Cookies.get("csrftoken"),
    },
  };

  try {
    await axios.post("/api/logout/", null, config);
    dispatch(logout());
  } catch (error) {
    toast.error(error.response.data.error);
  }
};

export const signUpAsync =
  (email, username, password, password2) => async (dispatch) => {
    const config = {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        "X-CSRFToken": Cookies.get("csrftoken"),
      },
    };

    const body = JSON.stringify({ email, username, password, password2 });
    try {
      const res = await axios.post("/api/signup/", body, config);
      if (res.status === 201) {
        dispatch(signup(res.data));
      }
    } catch (error) {
      toast.error(error.response.data.error);
    }
  };

export const checkAuthenticatedAsync = () => async (dispatch) => {
  const config = {
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
  };

  try {
    const res = await axios.get("/api/is_authenticated", config);
    if (res.status === 200) {
      dispatch(is_authenticated(res.data));
    }
  } catch (error) {
    toast.error(error);
  }
};

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    login: (state, action) => {
      state.isAuthenticated = true;
      state.user = action.payload.user;
      state.loading = false;
    },
    logout: (state) => {
      state.isAuthenticated = false;
      state.user = {};
    },
    signup: (state, action) => {
      state.isAuthenticated = true;
      state.user = action.payload.user;
      state.loading = false;
    },
    is_authenticated: (state, action) => {
      state.isAuthenticated = action.payload.isAuthenticated;
      state.user = action.payload.user;
      state.loading = false;
    },
  },
});

export const { login, logout, signup, is_authenticated } = authSlice.actions;
export default authSlice.reducer;
