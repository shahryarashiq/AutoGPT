"""
Job Search Block

This block searches for jobs across multiple platforms based on user criteria.
"""

from typing import Literal

from backend.data.block import Block, BlockCategory, BlockOutput, BlockSchema
from backend.data.model import SchemaField


class JobSearchBlock(Block):
    """
    Searches for jobs based on specified criteria across various job platforms.
    Returns a list of job postings matching the search criteria.
    """

    class Input(BlockSchema):
        platform: Literal["indeed", "linkedin", "gulftalent", "generic"] = SchemaField(
            description="Job platform to search on",
            default="generic"
        )
        job_titles: list[str] = SchemaField(
            description="List of desired job titles/positions (e.g., ['Cashier', 'Accountant', 'Sales Associate'])"
        )
        locations: list[str] = SchemaField(
            description="List of desired locations (e.g., ['Dubai, UAE', 'Abu Dhabi, UAE'])"
        )
        keywords: list[str] = SchemaField(
            description="Additional keywords to search for",
            default=[]
        )
        experience_level: str = SchemaField(
            description="Desired experience level (e.g., 'Entry Level', 'Mid Level', 'Senior')",
            default=""
        )
        max_results: int = SchemaField(
            description="Maximum number of job listings to return",
            default=50
        )

    class Output(BlockSchema):
        jobs: list[dict] = SchemaField(
            description="List of job postings found"
        )
        total_found: int = SchemaField(
            description="Total number of jobs found"
        )
        search_summary: str = SchemaField(
            description="Summary of the search performed"
        )

    def __init__(self):
        super().__init__(
            id="b2c3d4e5-6789-01bc-def2-2345678901bc",
            description="Searches for jobs on various platforms based on job titles, locations, and other criteria. Returns matching job listings.",
            categories={BlockCategory.SEARCH, BlockCategory.AI},
            input_schema=JobSearchBlock.Input,
            output_schema=JobSearchBlock.Output,
            test_input={
                "platform": "generic",
                "job_titles": ["Software Engineer"],
                "locations": ["Dubai, UAE"],
                "keywords": ["Python", "Backend"],
                "max_results": 10
            },
            test_output=[
                ("jobs", list),
                ("total_found", int),
                ("search_summary", str),
            ],
        )

    def run(self, input_data: Input, **kwargs) -> BlockOutput:
        """
        Search for jobs based on the provided criteria.
        
        Note: This is a mock implementation. In a production environment,
        you would integrate with actual job platform APIs.
        """
        
        # Build search query
        titles_str = ", ".join(input_data.job_titles)
        locations_str = ", ".join(input_data.locations)
        keywords_str = ", ".join(input_data.keywords) if input_data.keywords else "N/A"
        
        search_summary = f"Searching for {titles_str} in {locations_str} on {input_data.platform}"
        if input_data.keywords:
            search_summary += f" with keywords: {keywords_str}"
        
        # Mock job data - In production, this would call actual APIs
        mock_jobs = []
        
        for i, job_title in enumerate(input_data.job_titles):
            for j, location in enumerate(input_data.locations):
                if len(mock_jobs) >= input_data.max_results:
                    break
                    
                job = {
                    "id": f"job_{i}_{j}_{len(mock_jobs)}",
                    "title": job_title,
                    "company": f"Company {len(mock_jobs) + 1}",
                    "location": location,
                    "description": f"We are looking for a {job_title} to join our team in {location}. "
                                 f"Required skills: {', '.join(input_data.keywords[:3]) if input_data.keywords else 'Various skills'}. "
                                 f"Experience level: {input_data.experience_level if input_data.experience_level else 'Not specified'}.",
                    "platform": input_data.platform,
                    "url": f"https://{input_data.platform}.com/job/{len(mock_jobs) + 1}",
                    "posted_date": "2024-01-01",
                    "employment_type": "Full-time",
                    "salary_range": "Competitive",
                    "required_skills": input_data.keywords[:5] if input_data.keywords else [],
                }
                mock_jobs.append(job)
        
        total_found = len(mock_jobs)
        
        # Note for production: Here you would integrate with:
        # - Indeed API: https://opensource.indeedeng.io/api-documentation/
        # - LinkedIn API: Requires LinkedIn Partner Program access
        # - Gulf Talent: May require web scraping or direct partnership
        # - For free tier: Consider using RSS feeds, web scraping (with permission),
        #   or aggregator APIs like Adzuna, The Muse, etc.
        
        yield "jobs", mock_jobs
        yield "total_found", total_found
        yield "search_summary", search_summary
