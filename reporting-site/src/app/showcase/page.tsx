import type { Metadata } from "next";
import Showcase from "@/views/Showcase";

export const metadata: Metadata = {
  title: "Explorations",
  description:
    "Method experiments, evidence audits, and report surfaces built from public data, with source paths and caveats attached.",
};

export default function Page() {
  return <Showcase />;
}
