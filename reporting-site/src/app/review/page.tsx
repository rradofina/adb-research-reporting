import type { Metadata } from "next";
import ReviewDesk from "@/views/ReviewDesk";

export const metadata: Metadata = {
  title: "Researcher Review Desk",
  description:
    "Audit public-data measurement reports through their question, generated files, caveats, claim gates, and reproducibility path.",
};

export default function Page() {
  return <ReviewDesk />;
}
