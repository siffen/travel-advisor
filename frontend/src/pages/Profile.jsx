import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api";
import PlaceCard from "../components/PlaceCard";

export default function Profile({ user }) {
  const [favorites, setFavorites] = useState([]);
  useEffect(() => { api.favorites().then(setFavorites).catch(console.error); }, []);

  return (
    <div className="page-container profile-page">
      <div className="profile-card">
        <div className="avatar">{(user.full_name || user.username).charAt(0).toUpperCase()}</div>
        <div><div className="eyebrow">MY TRIPS</div><h1>{user.full_name || user.username}</h1><p>{user.email}</p></div>
      </div>
      <div className="profile-heading"><div><div className="eyebrow">SAVED DESTINATIONS</div><h2>Your shortlist</h2></div><Link to="/explore" className="primary-button">Find another place</Link></div>
      {favorites.length ? <div className="card-grid">{favorites.map((item) => <PlaceCard key={item.id} place={item.destination} />)}</div> : <div className="empty-state"><h3>Your shortlist is empty.</h3><p>Open any destination and tap “Save trip”.</p><Link to="/explore" className="primary-button">Explore destinations</Link></div>}
    </div>
  );
}
