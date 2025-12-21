"""
Resume Parser Block

This block parses uploaded resumes and extracts structured information.
"""

import re
from typing import Optional

from backend.data.block import Block, BlockCategory, BlockOutput, BlockSchema
from backend.data.model import SchemaField


class ResumeParserBlock(Block):
    """
    Parses a resume and extracts key information such as:
    - Contact information (name, email, phone)
    - Skills
    - Experience
    - Education
    - Summary/Objective
    """

    class Input(BlockSchema):
        resume_text: str = SchemaField(
            description="The text content of the resume to parse"
        )

    class Output(BlockSchema):
        name: str = SchemaField(
            description="Extracted name from resume", default=""
        )
        email: str = SchemaField(
            description="Extracted email address", default=""
        )
        phone: str = SchemaField(
            description="Extracted phone number", default=""
        )
        skills: list[str] = SchemaField(
            description="List of extracted skills", default=[]
        )
        experience: str = SchemaField(
            description="Work experience section", default=""
        )
        education: str = SchemaField(
            description="Education section", default=""
        )
        summary: str = SchemaField(
            description="Professional summary or objective", default=""
        )
        keywords: list[str] = SchemaField(
            description="Extracted keywords from the resume", default=[]
        )
        resume_text: str = SchemaField(
            description="Original resume text passed through for use in other blocks", default=""
        )

    def __init__(self):
        super().__init__(
            id="a1b2c3d4-5678-90ab-cdef-1234567890ab",
            description="Parses resume text and extracts structured information including contact details, skills, experience, and education",
            categories={BlockCategory.TEXT, BlockCategory.AI},
            input_schema=ResumeParserBlock.Input,
            output_schema=ResumeParserBlock.Output,
            test_input={
                "resume_text": "John Doe\nemail@example.com\n+1-234-567-8900\n\nSkills: Python, JavaScript, SQL\n\nExperience:\nSoftware Engineer at Tech Corp\n\nEducation:\nBS Computer Science"
            },
            test_output=[
                ("name", str),
                ("email", str),
                ("phone", str),
                ("skills", list),
                ("keywords", list),
            ],
        )

    def run(self, input_data: Input, **kwargs) -> BlockOutput:
        """
        Parse the resume and extract structured information.
        """
        resume_text = input_data.resume_text

        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, resume_text)
        email = email_match.group(0) if email_match else ""

        # Extract phone number
        phone_pattern = r'[\+]?[(]?[0-9]{1,4}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{1,4}[-\s\.]?[0-9]{1,9}'
        phone_match = re.search(phone_pattern, resume_text)
        phone = phone_match.group(0) if phone_match else ""

        # Extract name (assume first line or line before email)
        lines = resume_text.split('\n')
        name = ""
        for line in lines[:5]:  # Check first 5 lines
            line = line.strip()
            if line and not re.search(email_pattern, line) and not re.search(phone_pattern, line):
                if len(line.split()) >= 2 and len(line) < 50:  # Likely a name
                    name = line
                    break

        # Extract skills section
        skills = []
        skills_pattern = r'(?:Skills?|Technical Skills?|Core Competencies)[:：]?\s*(.*?)(?=\n\n|\n[A-Z]|$)'
        skills_match = re.search(skills_pattern, resume_text, re.IGNORECASE | re.DOTALL)
        if skills_match:
            skills_text = skills_match.group(1)
            # Split by common delimiters
            skills = [s.strip() for s in re.split(r'[,;•·\n]', skills_text) if s.strip()]

        # Extract experience section
        experience = ""
        exp_pattern = r'(?:Experience|Work Experience|Professional Experience)[:：]?\s*(.*?)(?=\n\n(?:Education|Skills)|$)'
        exp_match = re.search(exp_pattern, resume_text, re.IGNORECASE | re.DOTALL)
        if exp_match:
            experience = exp_match.group(1).strip()

        # Extract education section
        education = ""
        edu_pattern = r'(?:Education|Academic Background)[:：]?\s*(.*?)(?=\n\n(?:Experience|Skills)|$)'
        edu_match = re.search(edu_pattern, resume_text, re.IGNORECASE | re.DOTALL)
        if edu_match:
            education = edu_match.group(1).strip()

        # Extract summary/objective
        summary = ""
        summary_pattern = r'(?:Summary|Professional Summary|Objective|Career Objective)[:：]?\s*(.*?)(?=\n\n|$)'
        summary_match = re.search(summary_pattern, resume_text, re.IGNORECASE | re.DOTALL)
        if summary_match:
            summary = summary_match.group(1).strip()

        # Extract keywords (common job-related terms)
        keywords = []
        # Common technical and professional keywords
        keyword_patterns = [
            r'\b(?:Python|Java|JavaScript|TypeScript|C\+\+|SQL|HTML|CSS|React|Angular|Vue|Node\.js|Django|Flask|Spring|AWS|Azure|GCP|Docker|Kubernetes|Git|Agile|Scrum)\b',
            r'\b(?:Manager|Lead|Senior|Junior|Analyst|Engineer|Developer|Designer|Architect|Consultant|Specialist|Coordinator|Administrator)\b',
        ]
        
        for pattern in keyword_patterns:
            matches = re.findall(pattern, resume_text, re.IGNORECASE)
            keywords.extend([m for m in matches if m not in keywords])

        # Remove duplicates while preserving order
        keywords = list(dict.fromkeys(keywords))

        yield "name", name
        yield "email", email
        yield "phone", phone
        yield "skills", skills
        yield "experience", experience
        yield "education", education
        yield "summary", summary
        yield "keywords", keywords
        yield "resume_text", resume_text  # Pass through original text
