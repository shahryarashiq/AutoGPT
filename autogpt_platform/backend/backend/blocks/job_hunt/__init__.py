"""
Job Hunt Automation Blocks

This module provides blocks for automating job search and application processes.
"""

from .resume_parser import ResumeParserBlock
from .job_search import JobSearchBlock
from .resume_optimizer import ResumeOptimizerBlock
from .cover_letter_generator import CoverLetterGeneratorBlock
from .job_application_tracker import JobApplicationTrackerBlock

__all__ = [
    "ResumeParserBlock",
    "JobSearchBlock",
    "ResumeOptimizerBlock",
    "CoverLetterGeneratorBlock",
    "JobApplicationTrackerBlock",
]
