import type { Metadata } from "next";
import ShowcaseDataFreshness from "@/views/ShowcaseDataFreshness";
import { showcaseReports } from "@/data/showcaseReports";

const report = showcaseReports.find((r) => r.href === "/showcase/data-freshness");

export const metadata: Metadata = {
  title: report?.title,
  description: report?.deck,
};

export default function Page() {
  return <ShowcaseDataFreshness />;
}
