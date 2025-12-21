"use client";

import React, { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/__legacy__/ui/card";
import { Badge } from "@/components/__legacy__/ui/badge";
import { Button } from "@/components/atoms/Button";
import { Progress } from "@/components/atoms/Progress";
import {
  BarChart3,
  FileText,
  CheckCircle,
  Clock,
  XCircle,
  TrendingUp,
  ExternalLink,
} from "@phosphor-icons/react";

interface Application {
  id: string;
  jobTitle: string;
  company: string;
  location: string;
  platform: string;
  status: "pending" | "applied" | "interviewing" | "offered" | "rejected";
  appliedDate: string;
  matchScore: number;
  salary: string;
}

export default function ApplicationsDashboard() {
  const [applications] = useState<Application[]>([
    {
      id: "1",
      jobTitle: "Senior Accountant",
      company: "Dubai Finance Corp",
      location: "Dubai, UAE",
      platform: "Adzuna",
      status: "interviewing",
      appliedDate: "2024-12-15",
      matchScore: 85,
      salary: "AED 10,000 - 14,000",
    },
    {
      id: "2",
      jobTitle: "Cashier",
      company: "Retail Group UAE",
      location: "Abu Dhabi, UAE",
      platform: "Indeed",
      status: "applied",
      appliedDate: "2024-12-18",
      matchScore: 75,
      salary: "AED 4,000 - 6,000",
    },
    {
      id: "3",
      jobTitle: "Accounts Assistant",
      company: "Trading LLC",
      location: "Dubai, UAE",
      platform: "Adzuna",
      status: "rejected",
      appliedDate: "2024-12-10",
      matchScore: 65,
      salary: "AED 6,000 - 8,000",
    },
  ]);

  const statusConfig = {
    pending: { label: "Pending", icon: Clock, color: "bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-200" },
    applied: { label: "Applied", icon: FileText, color: "bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-200" },
    interviewing: { label: "Interviewing", icon: TrendingUp, color: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-200" },
    offered: { label: "Offered", icon: CheckCircle, color: "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-200" },
    rejected: { label: "Rejected", icon: XCircle, color: "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-200" },
  };

  const stats = {
    total: applications.length,
    pending: applications.filter((a) => a.status === "pending").length,
    applied: applications.filter((a) => a.status === "applied").length,
    interviewing: applications.filter((a) => a.status === "interviewing").length,
    offered: applications.filter((a) => a.status === "offered").length,
    rejected: applications.filter((a) => a.status === "rejected").length,
    avgMatchScore: Math.round(
      applications.reduce((sum, a) => sum + a.matchScore, 0) / applications.length
    ),
  };

  return (
    <div className="space-y-6">
      {/* Statistics Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="text-2xl font-bold">{stats.total}</div>
            <p className="text-sm text-gray-600 dark:text-gray-400">Total Applications</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="text-2xl font-bold text-blue-600">{stats.applied}</div>
            <p className="text-sm text-gray-600 dark:text-gray-400">Applied</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="text-2xl font-bold text-yellow-600">{stats.interviewing}</div>
            <p className="text-sm text-gray-600 dark:text-gray-400">Interviewing</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="text-2xl font-bold text-green-600">{stats.avgMatchScore}%</div>
            <p className="text-sm text-gray-600 dark:text-gray-400">Avg Match Score</p>
          </CardContent>
        </Card>
      </div>

      {/* Status Breakdown */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <BarChart3 className="w-5 h-5" />
            Application Status Breakdown
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {Object.entries(statusConfig).map(([status, config]) => {
            const count = stats[status as keyof typeof stats] as number;
            const percentage = (count / stats.total) * 100;
            return (
              <div key={status} className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="flex items-center gap-2">
                    <config.icon className="w-4 h-4" />
                    {config.label}
                  </span>
                  <span className="font-semibold">
                    {count} ({Math.round(percentage)}%)
                  </span>
                </div>
                <Progress value={percentage} className="h-2" />
              </div>
            );
          })}
        </CardContent>
      </Card>

      {/* Applications List */}
      <Card>
        <CardHeader>
          <CardTitle>Your Applications</CardTitle>
          <CardDescription>
            Track all your job applications in one place
          </CardDescription>
        </CardHeader>
        <CardContent>
          {applications.length === 0 ? (
            <div className="text-center py-12 text-gray-500">
              <p>No applications yet. Start searching for jobs to see them here!</p>
            </div>
          ) : (
            <div className="space-y-4">
              {applications.map((app) => {
                const StatusIcon = statusConfig[app.status].icon;
                return (
                  <Card key={app.id} className="hover:shadow-md transition-shadow">
                    <CardContent className="p-4">
                      <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-4">
                        <div className="flex-1">
                          <div className="flex items-start gap-3">
                            <div className="flex-1">
                              <h3 className="font-semibold text-lg">{app.jobTitle}</h3>
                              <p className="text-gray-600 dark:text-gray-400">
                                {app.company}
                              </p>
                              <div className="flex flex-wrap gap-2 mt-2 text-sm text-gray-500">
                                <span>📍 {app.location}</span>
                                <span>•</span>
                                <span>💰 {app.salary}</span>
                                <span>•</span>
                                <span>📅 Applied {app.appliedDate}</span>
                              </div>
                              <Badge variant="outline" className="mt-2">
                                via {app.platform}
                              </Badge>
                            </div>
                          </div>
                        </div>

                        <div className="flex flex-col items-end gap-2 min-w-[140px]">
                          <Badge className={statusConfig[app.status].color}>
                            <StatusIcon className="w-3 h-3 mr-1" />
                            {statusConfig[app.status].label}
                          </Badge>

                          <div className="text-right">
                            <div className="text-sm font-semibold">
                              Match: {app.matchScore}%
                            </div>
                            <Progress
                              value={app.matchScore}
                              className="h-1 w-24 mt-1"
                            />
                          </div>

                          <Button size="sm" variant="outline" className="mt-2">
                            <ExternalLink className="w-3 h-3 mr-1" />
                            View Details
                          </Button>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                );
              })}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
