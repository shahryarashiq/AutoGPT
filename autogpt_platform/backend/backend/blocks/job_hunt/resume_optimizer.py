"""
Resume Optimizer Block

This block optimizes a resume by adding relevant keywords from a job description.
"""

import re
from typing import Optional

from backend.data.block import Block, BlockCategory, BlockOutput, BlockSchema
from backend.data.model import SchemaField


class ResumeOptimizerBlock(Block):
    """
    Analyzes a job description and optimizes a resume by suggesting or adding
    relevant keywords that match the job requirements.
    """

    class Input(BlockSchema):
        resume_text: str = SchemaField(
            description="The current resume text"
        )
        job_description: str = SchemaField(
            description="The job description to optimize the resume for"
        )
        auto_add_keywords: bool = SchemaField(
            description="Whether to automatically add missing keywords to the resume",
            default=False
        )

    class Output(BlockSchema):
        optimized_resume: str = SchemaField(
            description="The optimized resume with added keywords"
        )
        missing_keywords: list[str] = SchemaField(
            description="Keywords from job description missing in the original resume"
        )
        matching_keywords: list[str] = SchemaField(
            description="Keywords that already match between resume and job description"
        )
        optimization_suggestions: str = SchemaField(
            description="Suggestions for further resume optimization"
        )
        match_score: float = SchemaField(
            description="Percentage match between resume and job description (0-100)"
        )

    def __init__(self):
        super().__init__(
            id="c3d4e5f6-7890-12cd-ef34-3456789012cd",
            description="Optimizes a resume by analyzing job descriptions and adding relevant keywords to improve match rate",
            categories={BlockCategory.TEXT, BlockCategory.AI},
            input_schema=ResumeOptimizerBlock.Input,
            output_schema=ResumeOptimizerBlock.Output,
            test_input={
                "resume_text": "Software Engineer with experience in web development",
                "job_description": "Looking for a Software Engineer with Python, Django, and React skills",
                "auto_add_keywords": True
            },
            test_output=[
                ("optimized_resume", str),
                ("missing_keywords", list),
                ("matching_keywords", list),
                ("match_score", float),
            ],
        )

    def _extract_keywords(self, text: str) -> set[str]:
        """
        Extract relevant keywords from text.
        Focus on technical skills, tools, and industry terms.
        """
        # Common technical and professional keywords patterns
        keyword_patterns = [
            # Programming languages
            r'\b(?:Python|Java|JavaScript|TypeScript|C\+\+|C#|Ruby|PHP|Go|Rust|Swift|Kotlin|Scala|R|MATLAB|Perl)\b',
            # Frameworks and libraries
            r'\b(?:React|Angular|Vue|Node\.js|Express|Django|Flask|Spring|Laravel|ASP\.NET|FastAPI|Next\.js|Nuxt)\b',
            # Databases
            r'\b(?:MySQL|PostgreSQL|MongoDB|Redis|SQLite|Oracle|SQL Server|DynamoDB|Cassandra|Neo4j)\b',
            # Cloud and DevOps
            r'\b(?:AWS|Azure|GCP|Docker|Kubernetes|Jenkins|GitLab|CircleCI|Terraform|Ansible|Chef|Puppet)\b',
            # Tools and platforms
            r'\b(?:Git|GitHub|Jira|Confluence|Slack|Visual Studio|IntelliJ|Eclipse|Postman|Figma|Sketch)\b',
            # Methodologies
            r'\b(?:Agile|Scrum|Kanban|DevOps|CI/CD|TDD|BDD|Microservices|REST|GraphQL|SOAP)\b',
            # Business skills
            r'\b(?:Project Management|Team Lead|Business Analysis|Data Analysis|Customer Service|Sales|Marketing|Finance|Accounting|HR)\b',
            # Soft skills and attributes
            r'\b(?:Leadership|Communication|Problem[- ]solving|Team[- ]work|Time Management|Critical Thinking|Adaptability)\b',
        ]
        
        keywords = set()
        text_lower = text.lower()
        
        for pattern in keyword_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            keywords.update([m.lower() for m in matches])
        
        return keywords

    def _calculate_match_score(self, resume_keywords: set[str], job_keywords: set[str]) -> float:
        """
        Calculate how well the resume matches the job description.
        """
        if not job_keywords:
            return 100.0
        
        matching = len(resume_keywords.intersection(job_keywords))
        total = len(job_keywords)
        
        return round((matching / total) * 100, 2)

    def _add_keywords_to_resume(self, resume_text: str, keywords_to_add: list[str]) -> str:
        """
        Add missing keywords to the resume in a natural way.
        """
        if not keywords_to_add:
            return resume_text
        
        # Check if there's a skills section
        skills_pattern = r'((?:Skills?|Technical Skills?|Core Competencies)[:：]?\s*)(.*?)(?=\n\n|\n[A-Z]|$)'
        skills_match = re.search(skills_pattern, resume_text, re.IGNORECASE | re.DOTALL)
        
        if skills_match:
            # Add to existing skills section
            header = skills_match.group(1)
            existing_skills = skills_match.group(2)
            new_skills = existing_skills.rstrip() + ", " + ", ".join(keywords_to_add)
            new_section = header + new_skills
            optimized = resume_text[:skills_match.start()] + new_section + resume_text[skills_match.end():]
        else:
            # Create a new skills section at the beginning (after name/contact)
            lines = resume_text.split('\n')
            insert_position = 0
            
            # Skip name, email, phone lines
            for i, line in enumerate(lines[:10]):
                if line.strip() and not re.search(r'@', line) and not re.search(r'\d{3}', line):
                    insert_position = i + 1
                elif re.search(r'\d{3}', line) or re.search(r'@', line):
                    insert_position = i + 1
            
            new_skills_section = f"\n\nSkills: {', '.join(keywords_to_add)}\n"
            lines.insert(insert_position, new_skills_section)
            optimized = '\n'.join(lines)
        
        return optimized

    def run(self, input_data: Input, **kwargs) -> BlockOutput:
        """
        Optimize the resume based on the job description.
        """
        resume_keywords = self._extract_keywords(input_data.resume_text)
        job_keywords = self._extract_keywords(input_data.job_description)
        
        # Find matching and missing keywords
        matching_keywords = list(resume_keywords.intersection(job_keywords))
        missing_keywords = list(job_keywords - resume_keywords)
        
        # Calculate match score
        match_score = self._calculate_match_score(resume_keywords, job_keywords)
        
        # Optimize resume if requested
        if input_data.auto_add_keywords and missing_keywords:
            optimized_resume = self._add_keywords_to_resume(
                input_data.resume_text, 
                missing_keywords[:10]  # Add top 10 missing keywords
            )
        else:
            optimized_resume = input_data.resume_text
        
        # Generate optimization suggestions
        suggestions = []
        if missing_keywords:
            suggestions.append(f"Consider adding these {len(missing_keywords)} keywords: {', '.join(missing_keywords[:5])}")
        if match_score < 50:
            suggestions.append("Your resume has a low match score. Consider tailoring it more closely to the job description.")
        elif match_score < 70:
            suggestions.append("Your resume is moderately matched. Adding more relevant keywords could improve your chances.")
        else:
            suggestions.append("Your resume is well-matched to this job description!")
        
        optimization_suggestions = " ".join(suggestions)
        
        yield "optimized_resume", optimized_resume
        yield "missing_keywords", missing_keywords
        yield "matching_keywords", matching_keywords
        yield "optimization_suggestions", optimization_suggestions
        yield "match_score", match_score
