import { Metadata } from "next";
import JobHuntDashboard from "./components/JobHuntDashboard";

export const metadata: Metadata = {
  title: "Job Hunt Automation - AutoGPT Platform",
  description: "Automate your job search with AI-powered resume optimization, job search, and application tracking",
  applicationName: "AutoGPT Job Hunt",
  authors: [{ name: "AutoGPT Team" }],
  keywords: [
    "job search",
    "resume optimization",
    "cover letter",
    "job automation",
    "AI jobs",
    "Dubai jobs",
    "UAE jobs",
    "AutoGPT",
  ],
};

export default function JobHuntPage() {
  return <JobHuntDashboard />;
}
