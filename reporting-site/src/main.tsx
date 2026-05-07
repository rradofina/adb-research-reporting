import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Layout from "./components/Layout";

// Editorial chrome
import Home from "./pages/Home";
import Research from "./pages/Research";
import Atlas from "./pages/Atlas";
import DMC from "./pages/DMC";
import Findings from "./pages/Findings";
import Briefs from "./pages/Briefs";
import Article from "./pages/Article";
import Evidence from "./pages/Evidence";
import Archive from "./pages/Archive";
import HowToRead from "./pages/HowToRead";
import Glossary from "./pages/Glossary";
import References from "./pages/References";
import About from "./pages/About";
import Team from "./pages/Team";
import DataCatalog from "./pages/DataCatalog";
import DataUpgrades from "./pages/DataUpgrades";
import Methods from "./pages/Methods";

// Existing program pages — preserved
import ProgramPSDQ from "./pages/ProgramPSDQ";
import ProgramAccessServices from "./pages/ProgramAccessServices";
import ProgramAirMonitoring from "./pages/ProgramAirMonitoring";
import ProgramRemittance from "./pages/ProgramRemittance";
import ProgramGrid from "./pages/ProgramGrid";
import ProgramDisaster from "./pages/ProgramDisaster";
import ProgramMigration from "./pages/ProgramMigration";
import ProgramPortFriction from "./pages/ProgramPortFriction";
import ProgramWaterCrop from "./pages/ProgramWaterCrop";
import ProgramClimateHealth from "./pages/ProgramClimateHealth";
import ProgramSocialProtection from "./pages/ProgramSocialProtection";
import ProgramSchoolHeat from "./pages/ProgramSchoolHeat";
import ProgramFoodPrice from "./pages/ProgramFoodPrice";

// Existing data surfaces — preserved as detail views
import CrossProgramMatrix from "./pages/CrossProgramMatrix";
import LiveData from "./pages/LiveData";
import Articles from "./pages/Articles";
import Methodology from "./pages/Methodology";
import Sources from "./pages/Sources";
import Reproducibility from "./pages/Reproducibility";

import NotFound from "./pages/NotFound";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          {/* Top-level editorial */}
          <Route path="/" element={<Home />} />
          <Route path="/research" element={<Research />} />
          <Route path="/atlas" element={<Atlas />} />
          <Route path="/dmc/:iso3" element={<DMC />} />
          <Route path="/findings" element={<Findings />} />
          <Route path="/briefs" element={<Briefs />} />
          <Route path="/findings/:slug" element={<Article />} />
          <Route path="/methods" element={<Methods />} />
          <Route path="/about" element={<About />} />
          <Route path="/team" element={<Team />} />

          {/* Data catalog & explorer */}
          <Route path="/data" element={<DataCatalog />} />
          <Route path="/data/explorer" element={<LiveData />} />
          <Route path="/data/matrix" element={<CrossProgramMatrix />} />
          <Route path="/data/upgrades" element={<DataUpgrades />} />
          <Route path="/archive" element={<Archive />} />
          <Route path="/how-to-read" element={<HowToRead />} />
          <Route path="/glossary" element={<Glossary />} />
          <Route path="/references" element={<References />} />

          {/* Program detail pages */}
          {/* Permanent evidence packets — §10.3 self-hosted archive */}
          <Route path="/program/:slug/evidence" element={<Evidence />} />
          <Route path="/program/public-service-data-quality" element={<ProgramPSDQ />} />
          <Route path="/program/access-services" element={<ProgramAccessServices />} />
          <Route path="/program/air-monitoring" element={<ProgramAirMonitoring />} />
          <Route path="/program/remittance-resilience" element={<ProgramRemittance />} />
          <Route path="/program/grid-reliability-heat" element={<ProgramGrid />} />
          <Route path="/program/disaster-recovery-lag" element={<ProgramDisaster />} />
          <Route path="/program/migration-displacement-signals" element={<ProgramMigration />} />
          <Route path="/program/port-hinterland-friction" element={<ProgramPortFriction />} />
          <Route path="/program/water-stress-crop-diversification" element={<ProgramWaterCrop />} />
          <Route path="/program/climate-health-workdays" element={<ProgramClimateHealth />} />
          <Route path="/program/social-protection-shock-coverage" element={<ProgramSocialProtection />} />
          <Route path="/program/school-heat-disruption" element={<ProgramSchoolHeat />} />
          <Route path="/program/food-price-climate-transmission" element={<ProgramFoodPrice />} />

          {/* Backward-compat redirects (Vercel-deployed bookmarks) */}
          <Route path="/live" element={<Navigate to="/data/explorer" replace />} />
          <Route path="/articles" element={<Navigate to="/findings" replace />} />
          <Route path="/matrix" element={<Navigate to="/data/matrix" replace />} />
          <Route path="/sources" element={<Navigate to="/data" replace />} />
          <Route path="/upgrades" element={<Navigate to="/data/upgrades" replace />} />
          <Route path="/methodology" element={<Methodology />} />
          <Route path="/reproducibility" element={<Reproducibility />} />

          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </BrowserRouter>
  </React.StrictMode>,
);
