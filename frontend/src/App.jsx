import { useEffect, useState } from "react";
import { Link, Navigate, Route, Routes, useLocation, useNavigate } from "react-router-dom";
import { api } from "./api";
import Home from "./pages/Home";
import Explore from "./pages/Explore";
import DestinationDetail from "./pages/DestinationDetail";
import Auth from "./pages/Auth";
import Profile from "./pages/Profile";
import BudgetCalculator from "./pages/BudgetCalculator";

export default function App() {
  const [user, setUser] = useState(null);
  const [authLoading, setAuthLoading] = useState(true);
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    if (!localStorage.getItem("travel_access_token")) {
      setAuthLoading(false);
      return;
    }
    api.me().then(setUser).catch(() => setUser(null)).finally(() => setAuthLoading(false));
  }, []);

  const logout = () => {
    localStorage.removeItem("travel_access_token");
    localStorage.removeItem("travel_refresh_token");
    setUser(null);
    navigate("/");
  };

  if (authLoading) {
    return <div className="app-loading"><div className="spinner" /> Loading Travel Advisor…</div>;
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <Link to="/" className="brand">
          <span className="brand-mark">✦</span>
          <span>Travel Advisor</span>
        </Link>
        <nav className="nav-links">
          <Link className={location.pathname === "/" ? "active" : ""} to="/">Home</Link>
          <Link className={location.pathname.startsWith("/explore") ? "active" : ""} to="/explore">Explore</Link>
          <Link className={location.pathname.startsWith("/budget") ? "active" : ""} to="/budget">Budget</Link>
          {user ? (
            <>
              <Link className={location.pathname === "/profile" ? "active" : ""} to="/profile">My Trips</Link>
              <button className="nav-button ghost" onClick={logout}>Log out</button>
            </>
          ) : (
            <Link className="nav-button" to="/auth">Sign in</Link>
          )}
        </nav>
      </header>

      <main>
        <Routes>
          <Route path="/" element={<Home user={user} />} />
          <Route path="/explore" element={<Explore user={user} />} />
          <Route path="/destination/:id" element={<DestinationDetail user={user} />} />
          <Route path="/budget" element={<BudgetCalculator />} />
          <Route path="/auth" element={user ? <Navigate to="/profile" replace /> : <Auth onAuth={setUser} />} />
          <Route path="/profile" element={user ? <Profile user={user} onLogout={logout} /> : <Navigate to="/auth" replace />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>

      <footer className="footer">
        <div><strong>Travel Advisor</strong> — discover places worth remembering.</div>
        <div className="footer-small">Built with React + Django + PostgreSQL</div>
      </footer>
    </div>
  );
}
