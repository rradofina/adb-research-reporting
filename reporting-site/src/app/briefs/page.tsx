import type { Metadata } from "next";
import Briefs from "@/views/Briefs";

export const metadata: Metadata = {
  title: "Briefs",
  description:
    "One-page briefs for each research program: the question, the current finding, and what the evidence cannot yet say.",
};

export default function Page() {
  return <Briefs />;
}
