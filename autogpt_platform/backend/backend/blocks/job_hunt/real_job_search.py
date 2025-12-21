"""
Real Job Platform Integration Block

This block provides real integration with free job search APIs.
"""

import os
from typing import Literal, Optional
import requests

from backend.data.block import Block, BlockCategory, BlockOutput, BlockSchema
from backend.data.model import SchemaField


class RealJobSearchBlock(Block):
    """
    Searches for jobs using real API integrations with free job platforms.
    Currently supports Adzuna (free API) and can be extended for other platforms.
    """

    class Input(BlockSchema):
        platform: Literal["adzuna"] = SchemaField(
            description="Job platform to search on (currently only Adzuna is supported with free API)",
            default="adzuna"
        )
        app_id: str = SchemaField(
            description="API Application ID (get free from https://developer.adzuna.com/)",
            default=""
        )
        app_key: str = SchemaField(
            description="API Application Key (get free from https://developer.adzuna.com/)",
            default=""
        )
        query: str = SchemaField(
            description="Job search query (e.g., 'accountant', 'cashier', 'software engineer')"
        )
        location: str = SchemaField(
            description="Location to search (e.g., 'Dubai', 'Abu Dhabi')",
            default=""
        )
        country_code: Literal["ae", "us", "uk", "ca", "au", "in", "sg"] = SchemaField(
            description="Country code for the search",
            default="ae"
        )
        results_per_page: int = SchemaField(
            description="Number of results to return (max 50)",
            default=20
        )
        page: int = SchemaField(
            description="Page number for pagination",
            default=1
        )
        sort_by: Literal["default", "date", "salary"] = SchemaField(
            description="How to sort the results",
            default="default"
        )

    class Output(BlockSchema):
        jobs: list[dict] = SchemaField(
            description="List of job postings found"
        )
        total_results: int = SchemaField(
            description="Total number of results available"
        )
        search_summary: str = SchemaField(
            description="Summary of the search performed"
        )
        error: str = SchemaField(
            description="Error message if search failed",
            default=""
        )

    def __init__(self):
        super().__init__(
            id="g7h8i9j0-1234-56gh-7890-7890123456gh",
            description="Searches for real jobs using Adzuna's free API. Supports multiple countries including UAE, US, UK, Canada, Australia, India, and Singapore.",
            categories={BlockCategory.SEARCH, BlockCategory.AI},
            input_schema=RealJobSearchBlock.Input,
            output_schema=RealJobSearchBlock.Output,
            test_input={
                "platform": "adzuna",
                "app_id": "test_app_id",
                "app_key": "test_app_key",
                "query": "software engineer",
                "location": "Dubai",
                "country_code": "ae",
                "results_per_page": 5
            },
            test_output=[
                ("jobs", list),
                ("total_results", int),
                ("search_summary", str),
            ],
            test_mock={
                "requests.get": lambda *args, **kwargs: type('Response', (), {
                    'json': lambda: {
                        "results": [
                            {
                                "id": "12345",
                                "title": "Software Engineer",
                                "company": {"display_name": "Tech Corp"},
                                "location": {"display_name": "Dubai"},
                                "description": "Great opportunity",
                                "salary_min": 5000,
                                "salary_max": 8000,
                                "redirect_url": "https://example.com/job/12345",
                                "created": "2024-01-01T00:00:00Z"
                            }
                        ],
                        "count": 1
                    },
                    'status_code': 200,
                    'raise_for_status': lambda: None
                })()
            }
        )

    def _search_adzuna(
        self,
        app_id: str,
        app_key: str,
        query: str,
        location: str,
        country_code: str,
        results_per_page: int,
        page: int,
        sort_by: str
    ) -> tuple[list[dict], int, str]:
        """
        Search jobs using Adzuna API.
        Documentation: https://developer.adzuna.com/docs/search
        """
        
        if not app_id or not app_key:
            raise ValueError(
                "Adzuna API credentials required. Get free credentials at https://developer.adzuna.com/"
            )
        
        # Build API URL
        url = f"https://api.adzuna.com/v1/api/jobs/{country_code}/search/{page}"
        
        # Build parameters
        params = {
            "app_id": app_id,
            "app_key": app_key,
            "results_per_page": min(results_per_page, 50),
            "what": query,
        }
        
        if location:
            params["where"] = location
        
        if sort_by == "date":
            params["sort_by"] = "date"
        elif sort_by == "salary":
            params["sort_by"] = "salary"
        
        # Make API request
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            # Parse results
            jobs = []
            for result in data.get("results", []):
                job = {
                    "id": str(result.get("id", "")),
                    "title": result.get("title", ""),
                    "company": result.get("company", {}).get("display_name", "N/A"),
                    "location": result.get("location", {}).get("display_name", "N/A"),
                    "description": result.get("description", "")[:500],  # First 500 chars
                    "salary_min": result.get("salary_min"),
                    "salary_max": result.get("salary_max"),
                    "salary_currency": result.get("salary_currency", "AED"),
                    "contract_type": result.get("contract_type", "Full-time"),
                    "url": result.get("redirect_url", ""),
                    "posted_date": result.get("created", ""),
                    "category": result.get("category", {}).get("label", ""),
                    "platform": "adzuna"
                }
                jobs.append(job)
            
            total_results = data.get("count", 0)
            search_summary = f"Found {total_results} jobs for '{query}'"
            if location:
                search_summary += f" in {location}"
            search_summary += f" ({country_code.upper()})"
            
            return jobs, total_results, search_summary
            
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"API request failed: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Failed to parse API response: {str(e)}")

    def run(self, input_data: Input, **kwargs) -> BlockOutput:
        """
        Search for jobs using the specified platform.
        """
        
        try:
            if input_data.platform == "adzuna":
                jobs, total_results, search_summary = self._search_adzuna(
                    app_id=input_data.app_id,
                    app_key=input_data.app_key,
                    query=input_data.query,
                    location=input_data.location,
                    country_code=input_data.country_code,
                    results_per_page=input_data.results_per_page,
                    page=input_data.page,
                    sort_by=input_data.sort_by
                )
                
                yield "jobs", jobs
                yield "total_results", total_results
                yield "search_summary", search_summary
            else:
                raise ValueError(f"Unsupported platform: {input_data.platform}")
                
        except Exception as e:
            yield "jobs", []
            yield "total_results", 0
            yield "search_summary", f"Search failed: {str(e)}"
            yield "error", str(e)
