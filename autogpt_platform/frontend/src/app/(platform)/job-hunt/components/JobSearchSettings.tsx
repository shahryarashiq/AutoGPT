"use client";

import React, { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/__legacy__/ui/card";
import { Button } from "@/components/atoms/Button";
import { Input } from "@/components/__legacy__/ui/input";
import { Label } from "@/components/__legacy__/ui/label";
import { Badge } from "@/components/__legacy__/ui/badge";
import { Search, Plus, X } from "@phosphor-icons/react";
import { CircleNotchIcon } from "@phosphor-icons/react/dist/ssr";

export default function JobSearchSettings() {
  const [jobTitles, setJobTitles] = useState<string[]>(["Cashier", "Accountant"]);
  const [newJobTitle, setNewJobTitle] = useState("");
  const [locations, setLocations] = useState<string[]>(["Dubai, UAE", "Abu Dhabi, UAE"]);
  const [newLocation, setNewLocation] = useState("");
  const [keywords, setKeywords] = useState<string[]>(["customer service", "QuickBooks"]);
  const [newKeyword, setNewKeyword] = useState("");
  const [searching, setSearching] = useState(false);
  const [searchResults, setSearchResults] = useState<any[]>([]);

  const addJobTitle = () => {
    if (newJobTitle.trim() && !jobTitles.includes(newJobTitle.trim())) {
      setJobTitles([...jobTitles, newJobTitle.trim()]);
      setNewJobTitle("");
    }
  };

  const removeJobTitle = (title: string) => {
    setJobTitles(jobTitles.filter((t) => t !== title));
  };

  const addLocation = () => {
    if (newLocation.trim() && !locations.includes(newLocation.trim())) {
      setLocations([...locations, newLocation.trim()]);
      setNewLocation("");
    }
  };

  const removeLocation = (location: string) => {
    setLocations(locations.filter((l) => l !== location));
  };

  const addKeyword = () => {
    if (newKeyword.trim() && !keywords.includes(newKeyword.trim())) {
      setKeywords([...keywords, newKeyword.trim()]);
      setNewKeyword("");
    }
  };

  const removeKeyword = (keyword: string) => {
    setKeywords(keywords.filter((k) => k !== keyword));
  };

  const handleSearch = async () => {
    setSearching(true);
    // Save settings to localStorage
    localStorage.setItem(
      "jobSearchSettings",
      JSON.stringify({ jobTitles, locations, keywords })
    );

    // Simulate search (in real implementation, this would call the JobSearchBlock)
    setTimeout(() => {
      setSearchResults([
        {
          id: "1",
          title: "Accountant",
          company: "Dubai Finance Corp",
          location: "Dubai, UAE",
          salary: "AED 8,000 - 12,000",
          matchScore: 85,
        },
        {
          id: "2",
          title: "Senior Cashier",
          company: "Retail Group UAE",
          location: "Abu Dhabi, UAE",
          salary: "AED 4,000 - 6,000",
          matchScore: 75,
        },
        {
          id: "3",
          title: "Accounts Assistant",
          company: "Trading LLC",
          location: "Dubai, UAE",
          salary: "AED 6,000 - 8,000",
          matchScore: 70,
        },
      ]);
      setSearching(false);
    }, 2000);
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Job Search Preferences</CardTitle>
          <CardDescription>
            Configure what jobs you're looking for and where. You can add multiple job titles and locations.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Job Titles */}
          <div className="space-y-3">
            <Label>Job Titles (Professions)</Label>
            <div className="flex flex-wrap gap-2 mb-2">
              {jobTitles.map((title) => (
                <Badge key={title} variant="secondary" className="pl-3 pr-1 py-1">
                  {title}
                  <Button
                    variant="ghost"
                    size="sm"
                    className="h-auto p-1 ml-1 hover:bg-transparent"
                    onClick={() => removeJobTitle(title)}
                  >
                    <X className="w-3 h-3" />
                  </Button>
                </Badge>
              ))}
            </div>
            <div className="flex gap-2">
              <Input
                placeholder="e.g., Sales Associate, Store Manager"
                value={newJobTitle}
                onChange={(e) => setNewJobTitle(e.target.value)}
                onKeyPress={(e) => e.key === "Enter" && addJobTitle()}
              />
              <Button onClick={addJobTitle} variant="outline">
                <Plus className="w-4 h-4" />
              </Button>
            </div>
          </div>

          {/* Locations */}
          <div className="space-y-3">
            <Label>Locations</Label>
            <div className="flex flex-wrap gap-2 mb-2">
              {locations.map((location) => (
                <Badge key={location} variant="secondary" className="pl-3 pr-1 py-1">
                  {location}
                  <Button
                    variant="ghost"
                    size="sm"
                    className="h-auto p-1 ml-1 hover:bg-transparent"
                    onClick={() => removeLocation(location)}
                  >
                    <X className="w-3 h-3" />
                  </Button>
                </Badge>
              ))}
            </div>
            <div className="flex gap-2">
              <Input
                placeholder="e.g., Sharjah, UAE or Ajman, UAE"
                value={newLocation}
                onChange={(e) => setNewLocation(e.target.value)}
                onKeyPress={(e) => e.key === "Enter" && addLocation()}
              />
              <Button onClick={addLocation} variant="outline">
                <Plus className="w-4 h-4" />
              </Button>
            </div>
          </div>

          {/* Keywords */}
          <div className="space-y-3">
            <Label>Keywords (Skills & Requirements)</Label>
            <div className="flex flex-wrap gap-2 mb-2">
              {keywords.map((keyword) => (
                <Badge key={keyword} variant="outline" className="pl-3 pr-1 py-1">
                  {keyword}
                  <Button
                    variant="ghost"
                    size="sm"
                    className="h-auto p-1 ml-1 hover:bg-transparent"
                    onClick={() => removeKeyword(keyword)}
                  >
                    <X className="w-3 h-3" />
                  </Button>
                </Badge>
              ))}
            </div>
            <div className="flex gap-2">
              <Input
                placeholder="e.g., cash handling, MS Office, SAP"
                value={newKeyword}
                onChange={(e) => setNewKeyword(e.target.value)}
                onKeyPress={(e) => e.key === "Enter" && addKeyword()}
              />
              <Button onClick={addKeyword} variant="outline">
                <Plus className="w-4 h-4" />
              </Button>
            </div>
          </div>

          <Button onClick={handleSearch} disabled={searching} className="w-full" size="lg">
            {searching ? (
              <>
                <CircleNotchIcon className="w-4 h-4 mr-2 animate-spin" />
                Searching Jobs...
              </>
            ) : (
              <>
                <Search className="w-4 h-4 mr-2" />
                Search for Jobs
              </>
            )}
          </Button>
        </CardContent>
      </Card>

      {searchResults.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Search Results</CardTitle>
            <CardDescription>
              Found {searchResults.length} matching jobs. Click on a job to see details and apply.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {searchResults.map((job) => (
                <Card key={job.id} className="hover:shadow-md transition-shadow">
                  <CardContent className="p-4">
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <h3 className="font-semibold text-lg">{job.title}</h3>
                        <p className="text-gray-600 dark:text-gray-400">{job.company}</p>
                        <p className="text-sm text-gray-500 dark:text-gray-500 mt-1">
                          📍 {job.location}
                        </p>
                        <p className="text-sm text-gray-500 dark:text-gray-500">
                          💰 {job.salary}
                        </p>
                      </div>
                      <div className="text-right">
                        <div className="mb-2">
                          <span
                            className={`inline-block px-3 py-1 rounded-full text-sm font-semibold ${
                              job.matchScore >= 80
                                ? "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-200"
                                : job.matchScore >= 60
                                ? "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-200"
                                : "bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-200"
                            }`}
                          >
                            {job.matchScore}% Match
                          </span>
                        </div>
                        <Button size="sm" className="mt-2">
                          View & Apply
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
