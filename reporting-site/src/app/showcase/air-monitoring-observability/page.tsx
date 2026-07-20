import type { Metadata } from "next";
import ShowcaseAirMonitoring from "@/views/ShowcaseAirMonitoring";
import { showcaseReports } from "@/data/showcaseReports";

const report = showcaseReports.find((r) => r.href === "/showcase/air-monitoring-observability");

export const metadata: Metadata = {
  title: report?.title,
  description: report?.deck,
};

export default function Page() {
  return <ShowcaseAirMonitoring />;
}
