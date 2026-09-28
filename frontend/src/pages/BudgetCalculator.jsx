import { useEffect, useMemo, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { api } from "../api";

const tiers = {
  budget: { label: "Budget", key: "daily_budget_low" },
  comfort: { label: "Comfort", key: "daily_budget_mid" },
  premium: { label: "Premium", key: "daily_budget_high" },
};

const formatINR = (value) => `₹${Math.round(value).toLocaleString("en-IN")}`;

export default function BudgetCalculator() {
  const [params] = useSearchParams();
  const [places, setPlaces] = useState([]);
  const [destinationId, setDestinationId] = useState(params.get("destination") || "");
  const [days, setDays] = useState(4);
  const [travelers, setTravelers] = useState(2);
  const [tier, setTier] = useState("comfort");
  const [longDistance, setLongDistance] = useState(8000);

  useEffect(() => {
    api.listDestinations("page_size=200").then((data) => setPlaces(data.results || data)).catch(console.error);
  }, []);

  const destination = useMemo(
    () => places.find((place) => String(place.id) === String(destinationId)),
    [places, destinationId]
  );

  const dailyPerPerson = destination ? Number(destination[tiers[tier].key] || 0) : 0;
  const dailyTotal = dailyPerPerson * travelers;
  const stayAndExperiences = dailyTotal * days;
  const longDistanceTotal = Number(longDistance || 0) * travelers;
  const total = stayAndExperiences + longDistanceTotal;
  const perPerson = total / Math.max(1, travelers);

  return (
    <div className="page-container budget-page">
      <div className="budget-heading">
        <div>
          <div className="eyebrow">TRIP PLANNER</div>
          <h1>Travel budget calculator</h1>
          <p>Estimate a trip in Indian rupees using the destination's indicative daily spend. Long-distance travel is added separately so you can enter your own flight, train or bus estimate.</p>
        </div>
        <Link to="/explore" className="section-link">← Explore destinations</Link>
      </div>

      <div className="budget-layout">
        <section className="budget-form-card">
          <div className="form-section-title">1. Choose your trip</div>
          <label>
            Destination
            <select value={destinationId} onChange={(e) => setDestinationId(e.target.value)}>
              <option value="">Select a destination</option>
              {places.map((place) => (
                <option key={place.id} value={place.id}>
                  {place.name} — {place.region === "India" ? `${place.state}, India` : place.country}
                </option>
              ))}
            </select>
          </label>

          <div className="budget-two-col">
            <label>
              Days
              <input type="number" min="1" max="30" value={days} onChange={(e) => setDays(Math.max(1, Math.min(30, Number(e.target.value) || 1)))} />
            </label>
            <label>
              Travelers
              <input type="number" min="1" max="12" value={travelers} onChange={(e) => setTravelers(Math.max(1, Math.min(12, Number(e.target.value) || 1)))} />
            </label>
          </div>

          <div className="form-section-title">2. Choose a travel style</div>
          <div className="tier-grid">
            {Object.entries(tiers).map(([key, item]) => (
              <button type="button" key={key} className={`tier-card ${tier === key ? "selected" : ""}`} onClick={() => setTier(key)}>
                <span>{item.label}</span>
                <strong>{destination ? formatINR(destination[item.key]) : "—"}</strong>
                <small>/ person / day</small>
              </button>
            ))}
          </div>

          <div className="form-section-title">3. Add your long-distance travel</div>
          <label>
            Travel cost per person (round trip)
            <input type="number" min="0" step="500" value={longDistance} onChange={(e) => setLongDistance(Math.max(0, Number(e.target.value) || 0))} />
          </label>
          <p className="helper-text">Tip: use your expected flight/train/bus cost from your home city. This calculator does not fetch live ticket prices.</p>
        </section>

        <aside className="budget-result-card">
          <div className="eyebrow">ESTIMATED TOTAL</div>
          <h2>{destination ? formatINR(total) : "Select a destination"}</h2>
          <p className="result-muted">{destination ? `${travelers} traveler${travelers === 1 ? "" : "s"} · ${days} day${days === 1 ? "" : "s"} · ${tiers[tier].label}` : "Your estimate will appear here."}</p>

          {destination && (
            <div className="budget-breakdown">
              <div><span>Daily destination spend</span><strong>{formatINR(dailyPerPerson)} / person</strong></div>
              <div><span>Stay + food + local + activities</span><strong>{formatINR(stayAndExperiences)}</strong></div>
              <div><span>Long-distance travel</span><strong>{formatINR(longDistanceTotal)}</strong></div>
              <div className="total-line"><span>Estimated per person</span><strong>{formatINR(perPerson)}</strong></div>
            </div>
          )}

          {destination && <Link to={`/destination/${destination.id}`} className="primary-button">View {destination.name}</Link>}
          <div className="estimate-note">Prices are indicative planning estimates in INR, not live quotes. Actual costs vary by dates, availability, hotel choice, transport and activities.</div>
        </aside>
      </div>
    </div>
  );
}
