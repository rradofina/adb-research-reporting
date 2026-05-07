import type { Metadata } from "next";
import { ProgramPage } from "@/components/research/ProgramPage";
import { getResearchProgram } from "@/data/research-programs";

const program = getResearchProgram("access-services");

export const metadata: Metadata = {
  title: `${program.title} | Development Blindspots Lab`,
  description: program.oneLine,
};

export default function AccessServicesPage() {
  return <ProgramPage program={program} />;
}
