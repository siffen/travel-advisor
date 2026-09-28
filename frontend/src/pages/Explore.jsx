import { useEffect, useMemo, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { api } from "../api";
import PlaceCard from "../components/PlaceCard";

const INDIA_STATES = [
  "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal", "Andaman and Nicobar Islands", "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu", "Delhi", "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry"
];

export default function Explore() {
  const [params, setParams] = useSearchParams();
  const [places, setPlaces] = useState([]);
  const [loading, setLoading] = useState(true);
  const [query, setQuery] = useState(params.get("search") || "");
  const region = params.get("region") || "";
  const state = params.get("state") || "";

  useEffect(() => {
    setLoading(true);
    const qs = new URLSearchParams();
    if (query) qs.set("search", query);
    if (region) qs.set("region", region);
    if (state) qs.set("state", state);
    qs.set("page_size", "160");
    api.listDestinations(qs.toString()).then((data) => setPlaces(data.results || data)).catch(console.error).finally(() => setLoading(false));
  }, [query, region, state]);

  const selectedLabel = useMemo(() => state || (region === "India" ? "All India" : region === "World" ? "World" : "All destinations"), [region, state]);

  const onRegionChange = (value) => {
    const next = new URLSearchParams(params);
    if (value) next.set("region", value); else next.delete("region");
    next.delete("state");
    setParams(next);
  };

  const onStateChange = (value) => {
    const next = new URLSearchParams(params);
    if (value) { next.set("region", "India"); next.set("state", value); } else next.delete("state");
    setParams(next);
  };

  return (
    <div className="page-container explore-page">
      <div className="explore-heading">
        <div><div className="eyebrow">DISCOVER</div><h1>Explore destinations</h1><p>Filter by region or Indian state, then open a place for more details.</p></div>
        <div className="result-count"><strong>{places.length}</strong><span>{selectedLabel}</span></div>
      </div>

      <div className="filters-panel">
        <div className="search-field"><span>⌕</span><input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Search a city or place" /></div>
        <select value={region} onChange={(e) => onRegionChange(e.target.value)}><option value="">All regions</option><option value="India">India</option><option value="World">World</option></select>
        <select value={state} disabled={region === "World"} onChange={(e) => onStateChange(e.target.value)}><option value="">All Indian states / UTs</option>{INDIA_STATES.map((item) => <option key={item}>{item}</option>)}</select>
      </div>

      {loading ? <div className="empty-state"><div className="spinner" /> Loading destinations…</div> : places.length ? <div className="card-grid">{places.map((place) => <PlaceCard key={place.id} place={place} featured={place.region === "World"} />)}</div> : <div className="empty-state"><h3>No destinations found</h3><p>Try another city, state or region.</p></div>}
    </div>
  );
}
