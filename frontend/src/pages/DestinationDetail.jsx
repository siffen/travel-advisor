import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { api } from "../api";

export default function DestinationDetail({ user }) {
  const { id } = useParams();
  const navigate = useNavigate();
  const [place, setPlace] = useState(null);
  const [saved, setSaved] = useState(false);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    api.getDestination(id).then(setPlace).catch(() => navigate("/explore"));
    if (user) api.favorites().then((items) => setSaved(items.some((item) => item.destination.id === Number(id)))).catch(() => {});
  }, [id, user, navigate]);

  if (!place) return <div className="app-loading"><div className="spinner" /> Loading destination…</div>;

  const toggleSave = async () => {
    if (!user) return navigate("/auth");
    setBusy(true);
    try {
      if (saved) await api.removeFavorite(place.id); else await api.addFavorite(place.id);
      setSaved(!saved);
    } finally { setBusy(false); }
  };

  const location = place.region === "India" ? `${place.city}, ${place.state}, India` : `${place.city}, ${place.country}`;

  return (
    <div className="detail-page">
      <div className="detail-hero" style={{ backgroundImage: `linear-gradient(0deg, rgba(4,14,11,.88), rgba(4,14,11,.08)), url(${place.image_url})` }}>
        <div className="detail-hero-inner page-container">
          <Link to="/explore" className="back-link">← Back to explore</Link>
          <div className="detail-heading">
            <div><span className="hero-badge">{place.country}</span><h1>{place.name}</h1><p>{location}</p></div>
            <button className={`save-button ${saved ? "saved" : ""}`} onClick={toggleSave} disabled={busy}>{saved ? "♥ Saved" : "♡ Save trip"}</button>
          </div>
        </div>
      </div>
      <div className="page-container detail-content">
        <article className="detail-main">
          <div className="eyebrow">ABOUT THIS PLACE</div>
          <h2>Why go</h2>
          <p className="lead">{place.description}</p>
          <div className="detail-tags">{(place.tags || []).map((tag) => <span className="tag" key={tag}>{tag}</span>)}</div>
        </article>
        <aside className="trip-facts">
          <div><span>Country</span><strong>{place.country}</strong></div>
          {place.state && <div><span>State / UT</span><strong>{place.state}</strong></div>}
          <div><span>Best time</span><strong>{place.best_time || "Year-round"}</strong></div>
          <div><span>Budget / person / day</span><strong>₹{Number(place.daily_budget_low || 0).toLocaleString("en-IN")} – ₹{Number(place.daily_budget_high || 0).toLocaleString("en-IN")}</strong></div>
          <div><span>Comfort estimate</span><strong>₹{Number(place.daily_budget_mid || 0).toLocaleString("en-IN")} / day</strong></div>
          <div><span>Region</span><strong>{place.region}</strong></div>
          <div><span>Price note</span><strong className="fact-note">{place.budget_note}</strong></div>
          <Link to={`/budget?destination=${place.id}`} className="primary-button budget-cta">Calculate this trip</Link>
        </aside>
      </div>
    </div>
  );
}
