"""
Job Application Tracker Block

This block tracks job applications and their status.
"""

from datetime import datetime
from typing import Literal, Optional

from backend.data.block import Block, BlockCategory, BlockOutput, BlockSchema
from backend.data.model import SchemaField


class JobApplicationTrackerBlock(Block):
    """
    Tracks job applications with their status, dates, and notes.
    Helps manage the job search process.
    """

    class Input(BlockSchema):
        action: Literal["add", "update", "get", "list_all"] = SchemaField(
            description="Action to perform: add new application, update existing, get specific, or list all"
        )
        job_id: str = SchemaField(
            description="Unique identifier for the job (required for update and get actions)",
            default=""
        )
        job_title: str = SchemaField(
            description="Title of the job position",
            default=""
        )
        company_name: str = SchemaField(
            description="Name of the company",
            default=""
        )
        location: str = SchemaField(
            description="Job location",
            default=""
        )
        platform: str = SchemaField(
            description="Platform where job was found (Indeed, LinkedIn, etc.)",
            default=""
        )
        job_url: str = SchemaField(
            description="URL to the job posting",
            default=""
        )
        status: Literal["pending", "applied", "interviewing", "offered", "rejected", "accepted", "withdrawn"] = SchemaField(
            description="Current status of the application",
            default="pending"
        )
        notes: str = SchemaField(
            description="Additional notes about the application",
            default=""
        )
        salary_range: str = SchemaField(
            description="Salary range if available",
            default=""
        )

    class Output(BlockSchema):
        success: bool = SchemaField(
            description="Whether the operation was successful"
        )
        message: str = SchemaField(
            description="Status message"
        )
        application_data: dict = SchemaField(
            description="Application data (for get action)",
            default={}
        )
        all_applications: list[dict] = SchemaField(
            description="List of all applications (for list_all action)",
            default=[]
        )
        statistics: dict = SchemaField(
            description="Statistics about applications",
            default={}
        )

    def __init__(self):
        # In-memory storage for demo purposes
        # In production, this would use a database
        self._applications = {}
        
        super().__init__(
            id="e5f6g7h8-9012-34ef-5678-5678901234ef",
            description="Tracks job applications with status updates, notes, and statistics. Manages the complete job application workflow.",
            categories={BlockCategory.BASIC, BlockCategory.TEXT},
            input_schema=JobApplicationTrackerBlock.Input,
            output_schema=JobApplicationTrackerBlock.Output,
            test_input={
                "action": "add",
                "job_id": "test_job_1",
                "job_title": "Software Engineer",
                "company_name": "Tech Corp",
                "location": "Dubai, UAE",
                "platform": "LinkedIn",
                "status": "pending"
            },
            test_output=[
                ("success", bool),
                ("message", str),
                ("statistics", dict),
            ],
        )

    def _generate_job_id(self, company_name: str, job_title: str) -> str:
        """Generate a unique job ID based on company and title."""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        base = f"{company_name}_{job_title}".replace(" ", "_").lower()
        return f"{base}_{timestamp}"

    def _add_application(self, input_data: Input) -> tuple[bool, str, dict]:
        """Add a new job application."""
        job_id = input_data.job_id or self._generate_job_id(
            input_data.company_name, input_data.job_title
        )
        
        if job_id in self._applications:
            return False, f"Application with ID {job_id} already exists", {}
        
        application = {
            "job_id": job_id,
            "job_title": input_data.job_title,
            "company_name": input_data.company_name,
            "location": input_data.location,
            "platform": input_data.platform,
            "job_url": input_data.job_url,
            "status": input_data.status,
            "notes": input_data.notes,
            "salary_range": input_data.salary_range,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }
        
        self._applications[job_id] = application
        return True, f"Successfully added application for {input_data.job_title} at {input_data.company_name}", application

    def _update_application(self, input_data: Input) -> tuple[bool, str, dict]:
        """Update an existing job application."""
        if not input_data.job_id:
            return False, "Job ID is required for update action", {}
        
        if input_data.job_id not in self._applications:
            return False, f"Application with ID {input_data.job_id} not found", {}
        
        application = self._applications[input_data.job_id]
        
        # Update fields if provided
        if input_data.job_title:
            application["job_title"] = input_data.job_title
        if input_data.company_name:
            application["company_name"] = input_data.company_name
        if input_data.location:
            application["location"] = input_data.location
        if input_data.platform:
            application["platform"] = input_data.platform
        if input_data.job_url:
            application["job_url"] = input_data.job_url
        if input_data.status:
            application["status"] = input_data.status
        if input_data.notes:
            application["notes"] = input_data.notes
        if input_data.salary_range:
            application["salary_range"] = input_data.salary_range
        
        application["updated_at"] = datetime.now().isoformat()
        
        return True, f"Successfully updated application {input_data.job_id}", application

    def _get_application(self, job_id: str) -> tuple[bool, str, dict]:
        """Get a specific job application."""
        if not job_id:
            return False, "Job ID is required for get action", {}
        
        if job_id not in self._applications:
            return False, f"Application with ID {job_id} not found", {}
        
        return True, "Application found", self._applications[job_id]

    def _list_all_applications(self) -> tuple[bool, str, list[dict]]:
        """List all job applications."""
        applications = list(self._applications.values())
        count = len(applications)
        return True, f"Found {count} application(s)", applications

    def _calculate_statistics(self) -> dict:
        """Calculate statistics about applications."""
        total = len(self._applications)
        if total == 0:
            return {
                "total_applications": 0,
                "by_status": {},
                "by_platform": {},
            }
        
        by_status = {}
        by_platform = {}
        
        for app in self._applications.values():
            status = app.get("status", "unknown")
            platform = app.get("platform", "unknown")
            
            by_status[status] = by_status.get(status, 0) + 1
            by_platform[platform] = by_platform.get(platform, 0) + 1
        
        return {
            "total_applications": total,
            "by_status": by_status,
            "by_platform": by_platform,
        }

    def run(self, input_data: Input, **kwargs) -> BlockOutput:
        """
        Execute the requested action on job applications.
        """
        success = False
        message = ""
        application_data = {}
        all_applications = []
        
        if input_data.action == "add":
            success, message, application_data = self._add_application(input_data)
        elif input_data.action == "update":
            success, message, application_data = self._update_application(input_data)
        elif input_data.action == "get":
            success, message, application_data = self._get_application(input_data.job_id)
        elif input_data.action == "list_all":
            success, message, all_applications = self._list_all_applications()
        else:
            message = f"Unknown action: {input_data.action}"
        
        statistics = self._calculate_statistics()
        
        yield "success", success
        yield "message", message
        yield "application_data", application_data
        yield "all_applications", all_applications
        yield "statistics", statistics
