import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { api } from "../api";

export default function Auth({ onAuth }) {
  const [mode, setMode] = useState("signin");
  const [form, setForm] = useState({ username: "", email: "", password: "", full_name: "" });
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const navigate = useNavigate();

  const update = (key) => (e) => setForm({ ...form, [key]: e.target.value });

  const submit = async (e) => {
    e.preventDefault(); setError(""); setBusy(true);
    try {
      const data = mode === "signin" ? await api.login({ username: form.username, password: form.password }) : await api.register(form);
      localStorage.setItem("travel_access_token", data.access);
      localStorage.setItem("travel_refresh_token", data.refresh);
      const me = data.user || await api.me();
      onAuth(me);
      navigate("/profile");
    } catch (err) { setError(err.message); } finally { setBusy(false); }
  };

  return (
    <div className="auth-page">
      <div className="auth-visual"><div><span className="hero-badge">TRAVEL ADVISOR</span><h1>Collect places.<br />Plan memories.</h1><p>Save the destinations that make you want to book a ticket.</p></div></div>
      <div className="auth-card-wrap">
        <div className="auth-card">
          <Link to="/" className="back-link">← Home</Link>
          <div className="auth-tabs"><button className={mode === "signin" ? "selected" : ""} onClick={() => setMode("signin")}>Sign in</button><button className={mode === "signup" ? "selected" : ""} onClick={() => setMode("signup")}>Create account</button></div>
          <h2>{mode === "signin" ? "Welcome back" : "Create your account"}</h2>
          <p className="auth-subtitle">{mode === "signin" ? "Use your Travel Advisor account to access saved trips." : "Your saved destinations will sync to this account."}</p>
          <form onSubmit={submit}>
            {mode === "signup" && <label>Full name<input value={form.full_name} onChange={update("full_name")} placeholder="Aarambh Tripathi" /></label>}
            <label>Username<input value={form.username} onChange={update("username")} placeholder="traveler123" autoComplete="username" required /></label>
            {mode === "signup" && <label>Email<input type="email" value={form.email} onChange={update("email")} placeholder="you@example.com" autoComplete="email" required /></label>}
            <label>Password<input type="password" value={form.password} onChange={update("password")} placeholder="Minimum 8 characters" autoComplete={mode === "signin" ? "current-password" : "new-password"} required minLength={8} /></label>
            {error && <div className="form-error">{error}</div>}
            <button className="submit-button" disabled={busy}>{busy ? "Please wait…" : mode === "signin" ? "Sign in" : "Create account"}</button>
          </form>
        </div>
      </div>
    </div>
  );
}
