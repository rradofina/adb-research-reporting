import type { Metadata } from "next";
import ShowcaseRemittanceFlow from "@/views/ShowcaseRemittanceFlow";
import { showcaseReports } from "@/data/showcaseReports";

const report = showcaseReports.find((r) => r.href === "/showcase/remittance-flow-weighting");

export const metadata: Metadata = {
  title: report?.title,
  description: report?.deck,
};

export default function Page() {
  return <ShowcaseRemittanceFlow />;
}
