import type { Metadata } from "next";
import ShowcaseDisasterMetric from "@/views/ShowcaseDisasterMetric";
import { showcaseReports } from "@/data/showcaseReports";

const report = showcaseReports.find((r) => r.href === "/showcase/disaster-metric-falsification");

export const metadata: Metadata = {
  title: report?.title,
  description: report?.deck,
};

export default function Page() {
  return <ShowcaseDisasterMetric />;
}
