import { useEffect, useMemo, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { api } from "../api";
import PlaceCard from "../components/PlaceCard";
import SectionHeader from "../components/SectionHeader";

const fallbackHero = "https://images.unsplash.com/photo-1469474968028-56623f02e42e?auto=format&fit=crop&w=1800&q=88";

export default function Home({ user }) {
  const [places, setPlaces] = useState([]);
  const [search, setSearch] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    api.listDestinations("featured=true&page_size=80").then((data) => setPlaces(data.results || data)).catch(console.error);
  }, []);

  const indianFeatured = useMemo(() => places.filter((p) => p.region === "India").slice(0, 10), [places]);
  const worldFeatured = useMemo(() => places.filter((p) => p.region === "World").slice(0, 8), [places]);
  const stateCount = useMemo(() => new Set(places.filter((p) => p.region === "India").map((p) => p.state)).size, [places]);

  const submitSearch = (event) => {
    event.preventDefault();
    navigate(`/explore${search.trim() ? `?search=${encodeURIComponent(search.trim())}` : ""}`);
  };

  return (
    <>
      <section className="hero" style={{ backgroundImage: `linear-gradient(90deg, rgba(5,20,15,.86), rgba(5,20,15,.35)), url(${fallbackHero})` }}>
        <div className="hero-content">
          <span className="hero-badge">✈ Curated travel inspiration</span>
          <h1>Go somewhere<br /><span>you’ll remember.</span></h1>
          <p>Search cities across every Indian state and discover iconic destinations around the world.</p>
          <form className="hero-search" onSubmit={submitSearch}>
            <span>⌕</span>
            <input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Search Jaipur, Bali, Varanasi…" />
            <button type="submit">Explore</button>
          </form>
          <div className="hero-stats">
            <div><strong>170+</strong><span>destinations</span></div>
            <div><strong>{stateCount || 36}</strong><span>Indian states & UTs</span></div>
            <div><strong>25+</strong><span>world picks</span></div>
          </div>
        </div>
      </section>

      <div className="page-container">
        <section className="section section-intro">
          <SectionHeader
            eyebrow="INDIA, STATE BY STATE"
            title="Start with India"
            subtitle="Browse major cities and travel bases across every state and Union Territory."
            linkText="Browse India"
            linkTo="/explore?region=India"
          />
          <div className="india-callout">
            <div className="india-callout-copy">
              <div className="eyebrow">Your next road trip</div>
              <h3>From Himalayan mornings to tropical sunsets.</h3>
              <p>Use the Explore page to filter by state, search a city, and open a destination guide.</p>
              <Link to="/explore?region=India" className="primary-button">Explore Indian cities</Link>
            </div>
            <img src="https://images.unsplash.com/photo-1524492412937-b28074a5d7da?auto=format&fit=crop&w=1000&q=84" alt="Taj Mahal" />
          </div>
        </section>

        <section className="section">
          <SectionHeader eyebrow="FEATURED INDIA" title="Places to put on your list" subtitle="A rotating set of featured Indian destinations." />
          <div className="card-grid">{indianFeatured.map((place) => <PlaceCard key={place.id} place={place} />)}</div>
        </section>

        <section className="section budget-promo">
          <div className="budget-promo-copy">
            <div className="eyebrow">PLAN YOUR SPEND</div>
            <h2>Know your trip budget before you book.</h2>
            <p>Pick a destination, number of days and travel style. The calculator gives an indicative per-person estimate in INR.</p>
            <Link to="/budget" className="primary-button">Open budget calculator →</Link>
          </div>
          <div className="budget-mini-grid">
            <div><span>STAY + FOOD</span><strong>Included</strong><small>Inside the daily destination estimate.</small></div>
            <div><span>LOCAL TRAVEL</span><strong>Included</strong><small>Inside the daily destination estimate.</small></div>
            <div><span>FLIGHTS / TRAIN</span><strong>Custom</strong><small>Add your own long-distance travel cost.</small></div>
          </div>
        </section>

        <section className="section">
          <SectionHeader eyebrow="AROUND THE WORLD" title="Big trips, one screen away" subtitle="Iconic cities, islands, mountain regions and heritage sites." linkText="Explore world" linkTo="/explore?region=World" />
          <div className="card-grid world-grid">{worldFeatured.map((place) => <PlaceCard key={place.id} place={place} featured />)}</div>
        </section>

        <section className="cta-banner">
          <div>
            <span className="eyebrow">SAVE YOUR PICKS</span>
            <h2>Build your personal trip shortlist.</h2>
            <p>{user ? "You’re signed in — open any place and save it to My Trips." : "Create a free account to save destinations and keep a personal shortlist."}</p>
          </div>
          <Link to={user ? "/profile" : "/auth"} className="primary-button light">{user ? "Open My Trips" : "Sign in to save"}</Link>
        </section>
      </div>
    </>
  );
}
