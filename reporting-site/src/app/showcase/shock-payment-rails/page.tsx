import type { Metadata } from "next";
import ShowcaseShockPayment from "@/views/ShowcaseShockPayment";
import { showcaseReports } from "@/data/showcaseReports";

const report = showcaseReports.find((r) => r.href === "/showcase/shock-payment-rails");

export const metadata: Metadata = {
  title: report?.title,
  description: report?.deck,
};

export default function Page() {
  return <ShowcaseShockPayment />;
}
