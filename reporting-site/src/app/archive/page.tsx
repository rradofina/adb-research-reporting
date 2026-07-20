import type { Metadata } from "next";
import Archive from "@/views/Archive";

export const metadata: Metadata = {
  title: "Archive",
  description:
    "Permanent, dated evidence archives for each research program, minted deterministically from the repository.",
};

export default function Page() {
  return <Archive />;
}
