import React from "react";
import { Routes, Route, Navigate, Link, useLocation } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Home from "./pages/Home";
import NotFound from "./pages/NotFound";
import ProtectedRoute from "./components/ProtectedRoute";
import UserPredictions from "./pages/UserPredictions";
import Account from "./pages/Account";
import NFLStatsChart from "./pages/NFLStatsChart";
import "./styles/App.css";

function Logout() {
  localStorage.clear();
  return <Navigate to="/login" />;
}

function RegisterAndLogout() {
  localStorage.clear();
  return <Register />;
}

function App() {
  const location = useLocation();

  const hideNavRoutes = ["/login", "/register"];

  return (
    <>
      {!hideNavRoutes.includes(location.pathname) && (
        <nav>
          <ul>
            <li>
              <Link to="/">Home</Link>
            </li>
            <li>
              <Link to="/account">Account</Link>
            </li>
            <li>
              <Link to="/account/predictions">My Predictions</Link>
            </li>
            <li>
              <Link to="/stats/nfl/team">NFL Team Stats</Link>
            </li>
            <li>
              <Link
                className="logout"
                to="/login"
                onClick={() => localStorage.clear()}
              >
                Logout
              </Link>
            </li>
          </ul>
        </nav>
      )}
      <Routes>
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Home />
            </ProtectedRoute>
          }
        />
        <Route
          path="/stats/nfl/team"
          element={
            <ProtectedRoute>
              <NFLStatsChart />
            </ProtectedRoute>
          }
        />
        <Route
          path="/account/predictions"
          element={
            <ProtectedRoute>
              <UserPredictions />
            </ProtectedRoute>
          }
        />
        <Route
          path="/account"
          element={
            <ProtectedRoute>
              <Account />
            </ProtectedRoute>
          }
        />
        <Route path="/login" element={<Login />} />
        <Route path="/logout" element={<Logout />} />
        <Route path="register" element={<RegisterAndLogout />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </>
  );
}

export default App;
