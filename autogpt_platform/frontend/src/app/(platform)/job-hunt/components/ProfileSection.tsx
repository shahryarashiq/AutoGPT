"use client";

import React, { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/__legacy__/ui/card";
import { Button } from "@/components/atoms/Button";
import { Input } from "@/components/__legacy__/ui/input";
import { Label } from "@/components/__legacy__/ui/label";
import { Textarea } from "@/components/__legacy__/ui/textarea";
import { Upload, User, Mail, Phone, FileText, Check } from "@phosphor-icons/react";

export default function ProfileSection() {
  const [profile, setProfile] = useState({
    name: "",
    email: "",
    phone: "",
    resumeText: "",
  });
  const [saved, setSaved] = useState(false);
  const [parsedData, setParsedData] = useState<any>(null);

  const handleResumeUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        const text = e.target?.result as string;
        setProfile({ ...profile, resumeText: text });
      };
      reader.readAsText(file);
    }
  };

  const handleSaveProfile = () => {
    // In a real implementation, this would call the ResumeParserBlock
    // For now, we'll just save locally
    localStorage.setItem("jobHuntProfile", JSON.stringify(profile));
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);

    // Simulate parsing
    setParsedData({
      skills: ["QuickBooks", "Excel", "SAP", "Financial Reporting"],
      experience: "4 years",
      keywords: ["Accountant", "Finance", "VAT"],
    });
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Your Profile</CardTitle>
          <CardDescription>
            Upload your resume or enter your information manually. This will be used to optimize applications for each job.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="name">
                <User className="w-4 h-4 inline mr-2" />
                Full Name
              </Label>
              <Input
                id="name"
                placeholder="John Doe"
                value={profile.name}
                onChange={(e) => setProfile({ ...profile, name: e.target.value })}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="email">
                <Mail className="w-4 h-4 inline mr-2" />
                Email
              </Label>
              <Input
                id="email"
                type="email"
                placeholder="john.doe@example.com"
                value={profile.email}
                onChange={(e) => setProfile({ ...profile, email: e.target.value })}
              />
            </div>

            <div className="space-y-2 md:col-span-2">
              <Label htmlFor="phone">
                <Phone className="w-4 h-4 inline mr-2" />
                Phone Number
              </Label>
              <Input
                id="phone"
                placeholder="+971-50-123-4567"
                value={profile.phone}
                onChange={(e) => setProfile({ ...profile, phone: e.target.value })}
              />
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="resume">
              <FileText className="w-4 h-4 inline mr-2" />
              Resume Text
            </Label>
            <Textarea
              id="resume"
              placeholder="Paste your resume here or upload a text file..."
              rows={10}
              value={profile.resumeText}
              onChange={(e) => setProfile({ ...profile, resumeText: e.target.value })}
              className="font-mono text-sm"
            />
          </div>

          <div className="flex items-center gap-4">
            <div>
              <Input
                id="resume-upload"
                type="file"
                accept=".txt"
                onChange={handleResumeUpload}
                className="hidden"
              />
              <Label htmlFor="resume-upload">
                <Button type="button" variant="outline" asChild>
                  <span>
                    <Upload className="w-4 h-4 mr-2" />
                    Upload Resume (.txt)
                  </span>
                </Button>
              </Label>
            </div>

            <Button onClick={handleSaveProfile} className="ml-auto">
              {saved ? (
                <>
                  <Check className="w-4 h-4 mr-2" />
                  Saved!
                </>
              ) : (
                "Save Profile"
              )}
            </Button>
          </div>

          {saved && (
            <div className="p-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg flex items-start gap-3">
              <Check className="w-5 h-5 text-green-600 dark:text-green-400 flex-shrink-0 mt-0.5" />
              <p className="text-sm text-green-800 dark:text-green-200">
                Profile saved successfully! Your resume will be used for job applications.
              </p>
            </div>
          )}
        </CardContent>
      </Card>

      {parsedData && (
        <Card>
          <CardHeader>
            <CardTitle>Parsed Resume Data</CardTitle>
            <CardDescription>
              We automatically extracted the following information from your resume
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div>
                <h4 className="font-semibold mb-2">Skills Identified:</h4>
                <div className="flex flex-wrap gap-2">
                  {parsedData.skills.map((skill: string, idx: number) => (
                    <span
                      key={idx}
                      className="px-3 py-1 bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-200 rounded-full text-sm"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              </div>

              <div>
                <h4 className="font-semibold mb-2">Keywords:</h4>
                <div className="flex flex-wrap gap-2">
                  {parsedData.keywords.map((keyword: string, idx: number) => (
                    <span
                      key={idx}
                      className="px-3 py-1 bg-purple-100 dark:bg-purple-900/30 text-purple-800 dark:text-purple-200 rounded-full text-sm"
                    >
                      {keyword}
                    </span>
                  ))}
                </div>
              </div>

              <div>
                <h4 className="font-semibold mb-2">Experience:</h4>
                <p className="text-gray-600 dark:text-gray-400">{parsedData.experience}</p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
