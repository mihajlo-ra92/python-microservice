import React from "react";
import { Link } from "react-router-dom";
import homeIcon from "../assets/logo-no-background-300px.svg";
import "../css/Navbar.css";
import useAuth from "../hooks/useAuth";
import { jwtDecode } from "jwt-decode";

const Navbar: React.FC = () => {
  const { isLoggedIn, logout } = useAuth();

  const getUserType = () => {
    const token = localStorage.getItem("token");
    if (token) {
      try {
        const decoded: {
          user_id: string;
          username: string;
          user_type: string;
          exp: number;
        } = jwtDecode(token);
        if (decoded && decoded.user_type) {
          return decoded.user_type;
        }
      } catch (error) {
        console.error("Error decoding JWT:", error);
      }
    }
    return null;
  };

  const userType = getUserType();
  return (
    <div className="navbar">
      <div className="left-options">
        <Link to="/">
          <img src={homeIcon} alt="Home" className="home-icon" />
        </Link>
      </div>
      <div className="right-options">
        {userType === "EMPLOYER" && <a href="/create-job">Post Job</a>}
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
