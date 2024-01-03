import { createContext, ReactNode, useState } from "react";

interface AuthContextProps {
  auth: Record<string, unknown>;
  setAuth: React.Dispatch<React.SetStateAction<Record<string, unknown>>>;
  isLoggedIn: boolean;
  login: () => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextProps | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({
  children,
}) => {
  const [auth, setAuth] = useState({});
  const [isLoggedIn, setLoggedIn] = useState(!!localStorage.getItem("token"));

  const login = () => {
    setLoggedIn(true);
  };

  const logout = () => {
    localStorage.removeItem("token");
    setLoggedIn(false);
  };

  return (
    <AuthContext.Provider value={{ auth, setAuth, isLoggedIn, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;
