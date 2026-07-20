import type { Metadata } from "next";
import About from "@/views/About";

export const metadata: Metadata = {
  title: "About",
  description:
    "What the Development Evidence Lab studies, how its research is produced and audited, and how AI assistance is disclosed.",
};

export default function Page() {
  return <About />;
}
