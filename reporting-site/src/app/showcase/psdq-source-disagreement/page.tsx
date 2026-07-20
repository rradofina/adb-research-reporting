import type { Metadata } from "next";
import ShowcasePSDQ from "@/views/ShowcasePSDQ";
import { showcaseReports } from "@/data/showcaseReports";

const report = showcaseReports.find((r) => r.href === "/showcase/psdq-source-disagreement");

export const metadata: Metadata = {
  title: report?.title,
  description: report?.deck,
};

export default function Page() {
  return <ShowcasePSDQ />;
}
