"use client";

import React, { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/__legacy__/ui/card";
import { Button } from "@/components/atoms/Button";
import { Input } from "@/components/__legacy__/ui/input";
import { Label } from "@/components/__legacy__/ui/label";
import { Badge } from "@/components/__legacy__/ui/badge";
import { Link as LinkIcon, Check, ExternalLink } from "@phosphor-icons/react";

interface Platform {
  id: string;
  name: string;
  description: string;
  connected: boolean;
  free: boolean;
  requiresApiKey: boolean;
  websiteUrl: string;
}

export default function PlatformConnections() {
  const [platforms, setPlatforms] = useState<Platform[]>([
    {
      id: "indeed",
      name: "Indeed",
      description: "Publisher API with free tier. Works great for UAE! Perfect if you already have an Indeed account.",
      connected: false,
      free: true,
      requiresApiKey: true,
      websiteUrl: "https://www.indeed.com/publisher",
    },
    {
      id: "adzuna",
      name: "Adzuna",
      description: "Free job search API with UAE support. No credit card required!",
      connected: false,
      free: true,
      requiresApiKey: true,
      websiteUrl: "https://developer.adzuna.com/",
    },
    {
      id: "linkedin",
      name: "LinkedIn",
      description: "Requires LinkedIn Partner access (not free). RSS feeds available as alternative.",
      connected: false,
      free: false,
      requiresApiKey: true,
      websiteUrl: "https://www.linkedin.com/developers/",
    },
    {
      id: "gulftalent",
      name: "Gulf Talent",
      description: "Best for UAE jobs. Contact them for API access.",
      connected: false,
      free: false,
      requiresApiKey: false,
      websiteUrl: "https://www.gulftalent.com/",
    },
  ]);

  const [credentials, setCredentials] = useState<Record<string, any>>({});

  const handleConnect = (platformId: string) => {
    // Save credentials to localStorage
    localStorage.setItem(`platform_${platformId}`, JSON.stringify(credentials[platformId]));

    // Update platform connection status
    setPlatforms(
      platforms.map((p) =>
        p.id === platformId ? { ...p, connected: true } : p
      )
    );
  };

  const handleDisconnect = (platformId: string) => {
    localStorage.removeItem(`platform_${platformId}`);
    setPlatforms(
      platforms.map((p) =>
        p.id === platformId ? { ...p, connected: false } : p
      )
    );
    setCredentials({ ...credentials, [platformId]: undefined });
  };

  const updateCredential = (platformId: string, field: string, value: string) => {
    setCredentials({
      ...credentials,
      [platformId]: {
        ...credentials[platformId],
        [field]: value,
      },
    });
  };

  return (
    <div className="space-y-6">
      <div className="p-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg">
        <p className="text-sm text-blue-800 dark:text-blue-200 mb-2">
          <strong>API Keys are Optional!</strong> You can use the dashboard without any API keys - 
          it will show demo jobs for testing.
        </p>
        <p className="text-sm text-blue-800 dark:text-blue-200">
          <strong>For real jobs:</strong> Connect Indeed if you have an account (takes 2 minutes, free).
          See <strong>HOW_TO_GET_INDEED_API.md</strong> for step-by-step guide with pictures.
        </p>
      </div>

      {platforms.map((platform) => (
        <Card key={platform.id}>
          <CardHeader>
            <div className="flex justify-between items-start">
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <CardTitle>{platform.name}</CardTitle>
                  {platform.free && (
                    <Badge variant="secondary" className="bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-200">
                      FREE
                    </Badge>
                  )}
                  {platform.connected && (
                    <Badge variant="default" className="bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-200">
                      <Check className="w-3 h-3 mr-1" />
                      Connected
                    </Badge>
                  )}
                </div>
                <CardDescription>{platform.description}</CardDescription>
              </div>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            {!platform.connected && platform.requiresApiKey && (
              <>
                {platform.id === "adzuna" && (
                  <div className="space-y-3">
                    <div>
                      <Label htmlFor={`${platform.id}-app-id`}>Application ID</Label>
                      <Input
                        id={`${platform.id}-app-id`}
                        placeholder="Your Adzuna App ID"
                        value={credentials[platform.id]?.appId || ""}
                        onChange={(e) =>
                          updateCredential(platform.id, "appId", e.target.value)
                        }
                      />
                    </div>
                    <div>
                      <Label htmlFor={`${platform.id}-app-key`}>Application Key</Label>
                      <Input
                        id={`${platform.id}-app-key`}
                        type="password"
                        placeholder="Your Adzuna App Key"
                        value={credentials[platform.id]?.appKey || ""}
                        onChange={(e) =>
                          updateCredential(platform.id, "appKey", e.target.value)
                        }
                      />
                    </div>
                  </div>
                )}

                {platform.id === "indeed" && (
                  <div>
                    <Label htmlFor={`${platform.id}-publisher-id`}>Publisher ID</Label>
                    <Input
                      id={`${platform.id}-publisher-id`}
                      placeholder="Your Indeed Publisher ID"
                      value={credentials[platform.id]?.publisherId || ""}
                      onChange={(e) =>
                        updateCredential(platform.id, "publisherId", e.target.value)
                      }
                    />
                  </div>
                )}

                {platform.id === "linkedin" && (
                  <div className="space-y-3">
                    <div>
                      <Label htmlFor={`${platform.id}-client-id`}>Client ID</Label>
                      <Input
                        id={`${platform.id}-client-id`}
                        placeholder="LinkedIn API Client ID"
                        value={credentials[platform.id]?.clientId || ""}
                        onChange={(e) =>
                          updateCredential(platform.id, "clientId", e.target.value)
                        }
                      />
                    </div>
                    <div>
                      <Label htmlFor={`${platform.id}-client-secret`}>Client Secret</Label>
                      <Input
                        id={`${platform.id}-client-secret`}
                        type="password"
                        placeholder="LinkedIn API Client Secret"
                        value={credentials[platform.id]?.clientSecret || ""}
                        onChange={(e) =>
                          updateCredential(platform.id, "clientSecret", e.target.value)
                        }
                      />
                    </div>
                  </div>
                )}
              </>
            )}

            <div className="flex gap-2">
              {!platform.connected && platform.requiresApiKey ? (
                <>
                  <Button
                    variant="outline"
                    onClick={() => window.open(platform.websiteUrl, "_blank")}
                  >
                    <ExternalLink className="w-4 h-4 mr-2" />
                    Get API Key
                  </Button>
                  <Button
                    onClick={() => handleConnect(platform.id)}
                    disabled={
                      (platform.id === "adzuna" &&
                        (!credentials[platform.id]?.appId ||
                          !credentials[platform.id]?.appKey)) ||
                      (platform.id === "indeed" &&
                        !credentials[platform.id]?.publisherId)
                    }
                  >
                    <LinkIcon className="w-4 h-4 mr-2" />
                    Connect
                  </Button>
                </>
              ) : !platform.connected && !platform.requiresApiKey ? (
                <Button
                  variant="outline"
                  onClick={() => window.open(platform.websiteUrl, "_blank")}
                >
                  <ExternalLink className="w-4 h-4 mr-2" />
                  Visit Website
                </Button>
              ) : (
                <Button
                  variant="destructive"
                  onClick={() => handleDisconnect(platform.id)}
                >
                  Disconnect
                </Button>
              )}
            </div>
          </CardContent>
        </Card>
      ))}

      <Card className="bg-gray-50 dark:bg-gray-900/50">
        <CardHeader>
          <CardTitle>Need Help?</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
            Check out our{" "}
            <a
              href="/JOB_PLATFORM_INTEGRATION.md"
              className="text-blue-600 dark:text-blue-400 underline"
            >
              Platform Integration Guide
            </a>{" "}
            for detailed instructions on getting API keys and connecting each platform.
          </p>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            <strong>Quick Tip:</strong> Indeed is the easiest if you already have an account - just register for a Publisher ID at indeed.com/publisher. It's free and takes 2 minutes!
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
