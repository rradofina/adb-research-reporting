import type { Metadata } from "next";
import Doc from "@/views/Doc";

export const metadata: Metadata = {
  title: "Status board",
  description:
    "The live operating board: active flagship program, stage, queue, and verification status.",
};

export default function Page() {
  return <Doc name="status" />;
}
