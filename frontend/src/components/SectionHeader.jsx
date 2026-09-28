import { Link } from "react-router-dom";

export default function SectionHeader({ eyebrow, title, subtitle, linkText = "View all", linkTo = "/explore" }) {
  return (
    <div className="section-header">
      <div>
        {eyebrow && <div className="eyebrow">{eyebrow}</div>}
        <h2>{title}</h2>
        {subtitle && <p>{subtitle}</p>}
      </div>
      {linkText && <Link to={linkTo} className="section-link">{linkText} →</Link>}
    </div>
  );
}
