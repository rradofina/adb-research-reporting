import type { Metadata } from "next";
import Research from "@/views/Research";

export const metadata: Metadata = {
  title: "Research programs",
  description:
    "All registered research programs by domain, each with an authoritative maturity label and a route into its public-data evidence.",
};

export default function Page() {
  return <Research />;
}
