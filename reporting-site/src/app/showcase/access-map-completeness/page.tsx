import type { Metadata } from "next";
import ShowcaseAccessCompleteness from "@/views/ShowcaseAccessCompleteness";
import { showcaseReports } from "@/data/showcaseReports";

const report = showcaseReports.find((r) => r.href === "/showcase/access-map-completeness");

export const metadata: Metadata = {
  title: report?.title,
  description: report?.deck,
};

export default function Page() {
  return <ShowcaseAccessCompleteness />;
}
