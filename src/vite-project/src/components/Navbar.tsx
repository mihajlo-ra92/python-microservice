import React from "react";
import { Link } from "react-router-dom";
import homeIcon from "../assets/logo-no-background-300px.svg";
import "./Navbar.css";

const Navbar: React.FC = () => {
  return (
    <div className="navbar">
      <div className="left-options">
        <Link to="/">
          <img src={homeIcon} alt="Home" className="home-icon" />
        </Link>
      </div>
      <div className="right-options">
        <a href="#">About</a>
        <a href="#">Services</a>
        <a href="/register">Register</a>
        <a href="/login">Login</a>
      </div>
    </div>
  );
};

export default Navbar;
