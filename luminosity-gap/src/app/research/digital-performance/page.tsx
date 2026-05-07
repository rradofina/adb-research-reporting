import type { Metadata } from "next";
import { ProgramPage } from "@/components/research/ProgramPage";
import { getResearchProgram } from "@/data/research-programs";

const program = getResearchProgram("digital-performance");

export const metadata: Metadata = {
  title: `${program.title} | Development Blindspots Lab`,
  description: program.oneLine,
};

export default function DigitalPerformancePage() {
  return <ProgramPage program={program} />;
}
