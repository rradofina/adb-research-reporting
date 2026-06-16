/**
 * main.tsx — three active surfaces + governance docs + redirects.
 *
 * Active surfaces:
 *   /                    Home (topic list)
 *   /:slug               Topic page (unified, with tabs)
 *   /about               About
 *   /docs                Index of governance documents
 *   /{doc-slug}          One governance document (Constitution, etc.)
 *
 * Governance doc slugs (constitution, factory, operating-rules, etc.)
 * are reserved — declared explicitly before /:slug so the topic
 * catch-all does not eat them.
 */
import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route, Navigate, useParams } from "react-router-dom";
import Layout from "./components/Layout";
import Home from "./pages/Home";
import Topic from "./pages/Topic";
import NativeCharts from "./pages/NativeCharts";
import NativeDeepenings from "./pages/NativeDeepenings";
import Showcase from "./pages/Showcase";
import ShowcaseDataFreshness from "./pages/ShowcaseDataFreshness";
import ShowcaseShockPayment from "./pages/ShowcaseShockPayment";
import ShowcasePSDQ from "./pages/ShowcasePSDQ";
import ShowcaseRemittanceFlow from "./pages/ShowcaseRemittanceFlow";
import ShowcaseAirMonitoring from "./pages/ShowcaseAirMonitoring";
import ShowcaseAccessCompleteness from "./pages/ShowcaseAccessCompleteness";
import About from "./pages/About";
import Doc from "./pages/Doc";
import Docs from "./pages/Docs";
import NotFound from "./pages/NotFound";
import "./index.css";

function ProgramEvidenceRedirect() {
  const { slug = "" } = useParams();
  return <Navigate to={`/${slug}?view=evidence`} replace />;
}

function ProgramRedirect() {
  const { slug = "" } = useParams();
  return <Navigate to={`/${slug}`} replace />;
}

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          {/* === Top-level surfaces === */}
          <Route path="/" element={<Home />} />
          <Route path="/native-charts" element={<NativeCharts />} />
          <Route path="/deepenings" element={<NativeDeepenings />} />
          <Route path="/showcase" element={<Showcase />} />
          <Route path="/showcase/data-freshness" element={<ShowcaseDataFreshness />} />
          <Route path="/showcase/shock-payment-rails" element={<ShowcaseShockPayment />} />
          <Route path="/showcase/psdq-source-disagreement" element={<ShowcasePSDQ />} />
          <Route path="/showcase/remittance-flow-weighting" element={<ShowcaseRemittanceFlow />} />
          <Route path="/showcase/air-monitoring-observability" element={<ShowcaseAirMonitoring />} />
          <Route path="/showcase/access-map-completeness" element={<ShowcaseAccessCompleteness />} />
          <Route path="/about" element={<About />} />
          <Route path="/docs" element={<Docs />} />

          {/* === Governance documents (in-site rendering) === */}
          <Route path="/constitution" element={<Doc name="constitution" />} />
          <Route path="/operating-rules" element={<Doc name="operating-rules" />} />
          <Route path="/agents" element={<Doc name="agents" />} />
          <Route path="/factory" element={<Doc name="factory" />} />
          <Route path="/status" element={<Doc name="status" />} />
          <Route path="/wip-register" element={<Doc name="wip-register" />} />
          <Route path="/red-team" element={<Doc name="red-team" />} />
          <Route path="/data-access-audit" element={<Doc name="data-access-audit" />} />
          <Route path="/sources" element={<Doc name="sources" />} />
          <Route path="/repo-readme" element={<Doc name="repo-readme" />} />
          <Route path="/license" element={<Doc name="license" />} />
          <Route path="/license-content" element={<Doc name="license-content" />} />
          <Route path="/versions" element={<Doc name="versions" />} />
          <Route path="/manifest" element={<Doc name="manifest" />} />

          {/* === Backward-compat redirects (must come BEFORE /:slug) === */}
          <Route path="/findings" element={<Navigate to="/" replace />} />
          <Route path="/findings/:slug" element={<Navigate to="/" replace />} />
          <Route path="/articles" element={<Navigate to="/" replace />} />
          <Route path="/articles/:slug" element={<Navigate to="/" replace />} />
          <Route path="/program/:slug/evidence" element={<ProgramEvidenceRedirect />} />
          <Route path="/program/:slug" element={<ProgramRedirect />} />
          <Route path="/research" element={<Navigate to="/" replace />} />
          <Route path="/atlas" element={<Navigate to="/" replace />} />
          <Route path="/dmc/:iso3" element={<Navigate to="/" replace />} />
          <Route path="/briefs" element={<Navigate to="/" replace />} />
          <Route path="/methods" element={<Navigate to="/about" replace />} />
          <Route path="/methodology" element={<Navigate to="/about" replace />} />
          <Route path="/reproducibility" element={<Navigate to="/about" replace />} />
          <Route path="/team" element={<Navigate to="/about" replace />} />
          <Route path="/data" element={<Navigate to="/" replace />} />
          <Route path="/data/explorer" element={<Navigate to="/" replace />} />
          <Route path="/data/matrix" element={<Navigate to="/" replace />} />
          <Route path="/data/upgrades" element={<Navigate to="/" replace />} />
          <Route path="/archive" element={<Navigate to="/" replace />} />
          <Route path="/how-to-read" element={<Navigate to="/about" replace />} />
          <Route path="/glossary" element={<Navigate to="/about" replace />} />
          <Route path="/references" element={<Navigate to="/about" replace />} />
          <Route path="/live" element={<Navigate to="/" replace />} />
          <Route path="/matrix" element={<Navigate to="/" replace />} />
          <Route path="/upgrades" element={<Navigate to="/" replace />} />

          {/* === Topic catch-all (LAST among Layout-wrapped routes) === */}
          <Route path="/:slug" element={<Topic />} />

          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </BrowserRouter>
  </React.StrictMode>,
);
