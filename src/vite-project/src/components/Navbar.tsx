import React from "react";
import { Link } from "react-router-dom";
import homeIcon from "../assets/logo-no-background-300px.svg";
import "../css/Navbar.css";
import useAuth from "../hooks/useAuth";

const Navbar: React.FC = () => {
  const { isLoggedIn, logout } = useAuth();

  return (
    <div className="navbar">
      <div className="left-options">
        <Link to="/">
          <img src={homeIcon} alt="Home" className="home-icon" />
        </Link>
      </div>
      <div className="right-options">
        <a href="/create-job">Post Job</a>
        <a />
        <a href="#">Services</a>
        <a />
        {!isLoggedIn && <a href="/register">Register</a>}
        <a />
        {!isLoggedIn && <a href="/login">Login</a>}
        <a />
        {isLoggedIn && (
          <a href="/" onClick={logout}>
            Logout
          </a>
        )}
      </div>
    </div>
  );
};

export default Navbar;
