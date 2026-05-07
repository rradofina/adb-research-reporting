import { Link } from "react-router-dom";
import { Kicker } from "../components/ui";

export default function NotFound() {
  return (
    <div className="py-24 text-center">
      <Kicker>Page not found</Kicker>
      <h1 className="masthead-display text-[clamp(3rem,8vw,6rem)] mt-4">
        № <span className="display-italic" style={{ color: "var(--crimson)" }}>404</span>
      </h1>
      <p className="lede mt-6 max-w-[40ch] mx-auto">
        That page doesn't exist on this issue. Try the index, or search the
        atlas for an economy.
      </p>
      <div className="mt-8 flex justify-center gap-4 flex-wrap">
        <Link to="/" className="ed-link">Home</Link>
        <Link to="/research" className="ed-link">Research</Link>
        <Link to="/atlas" className="ed-link">Atlas</Link>
        <Link to="/findings" className="ed-link">Findings</Link>
      </div>
    </div>
  );
}
