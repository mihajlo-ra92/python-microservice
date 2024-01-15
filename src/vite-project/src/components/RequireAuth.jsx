import { useLocation, Navigate, Outlet } from "react-router-dom";
import { jwtDecode } from "jwt-decode";
import useAuth from "../hooks/useAuth";

const RequireAuth = ({ allowedRoles }) => {
  const { isLoggedIn } = useAuth();
  const location = useLocation();
  const token = localStorage.getItem("token");
  const decodedToken = token ? jwtDecode(token) : null;

  return allowedRoles.includes(decodedToken?.user_type) ? (
    <Outlet />
  ) : isLoggedIn ? (
    <Navigate to="/unauthorized" state={{ from: location }} replace />
  ) : (
    <Navigate to="/login" state={{ from: location }} replace />
  );
};

export default RequireAuth;
