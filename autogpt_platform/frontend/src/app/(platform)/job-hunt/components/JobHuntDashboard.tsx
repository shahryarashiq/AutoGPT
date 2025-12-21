"use client";

import React, { useState } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/__legacy__/ui/tabs";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/__legacy__/ui/card";
import ProfileSection from "./ProfileSection";
import JobSearchSettings from "./JobSearchSettings";
import PlatformConnections from "./PlatformConnections";
import ApplicationsDashboard from "./ApplicationsDashboard";
import { FileText, Search, Link, BarChart3 } from "@phosphor-icons/react";

export default function JobHuntDashboard() {
  const [activeTab, setActiveTab] = useState("profile");

  return (
    <div className="container mx-auto p-6 max-w-7xl">
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-2">Job Hunt Automation</h1>
        <p className="text-gray-600 dark:text-gray-400">
          Automate your job search with AI-powered tools. Search for jobs, optimize your resume, and track applications.
        </p>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList className="grid w-full grid-cols-4 lg:w-auto lg:inline-grid">
          <TabsTrigger value="profile" className="flex items-center gap-2">
            <FileText className="w-4 h-4" />
            <span className="hidden sm:inline">Profile & Resume</span>
            <span className="sm:hidden">Profile</span>
          </TabsTrigger>
          <TabsTrigger value="search" className="flex items-center gap-2">
            <Search className="w-4 h-4" />
            <span className="hidden sm:inline">Job Search</span>
            <span className="sm:hidden">Search</span>
          </TabsTrigger>
          <TabsTrigger value="platforms" className="flex items-center gap-2">
            <Link className="w-4 h-4" />
            <span className="hidden sm:inline">Platforms</span>
            <span className="sm:hidden">Connect</span>
          </TabsTrigger>
          <TabsTrigger value="applications" className="flex items-center gap-2">
            <BarChart3 className="w-4 h-4" />
            <span className="hidden sm:inline">Applications</span>
            <span className="sm:hidden">Apps</span>
          </TabsTrigger>
        </TabsList>

        <TabsContent value="profile" className="space-y-4">
          <ProfileSection />
        </TabsContent>

        <TabsContent value="search" className="space-y-4">
          <JobSearchSettings />
        </TabsContent>

        <TabsContent value="platforms" className="space-y-4">
          <PlatformConnections />
        </TabsContent>

        <TabsContent value="applications" className="space-y-4">
          <ApplicationsDashboard />
        </TabsContent>
      </Tabs>
    </div>
  );
}
