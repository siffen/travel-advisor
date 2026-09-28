import { Link } from "react-router-dom";

export default function PlaceCard({ place, featured = false }) {
  return (
    <Link to={`/destination/${place.id}`} className={`place-card ${featured ? "featured-card" : ""}`}>
      <div className="place-image-wrap">
        <img src={place.image_url} alt={place.name} className="place-image" loading="lazy" />
        {place.is_featured && <span className="featured-pill">Featured</span>}
      </div>
      <div className="place-card-body">
        <div className="place-kicker">{place.region === "India" ? `${place.city}, ${place.state}` : `${place.city}, ${place.country}`}</div>
        <h3>{place.name}</h3>
        <p>{place.description}</p>
        <div className="tag-row">
          {(place.tags || []).slice(0, 3).map((tag) => <span key={tag} className="tag">{tag}</span>)}
        </div>
        <div className="price-strip">
          <span>From</span>
          <strong>₹{Number(place.daily_budget_low || 0).toLocaleString("en-IN")}</strong>
          <small>/ person / day</small>
        </div>
      </div>
    </Link>
  );
}
