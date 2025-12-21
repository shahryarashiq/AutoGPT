"""
Cover Letter Generator Block

This block generates customized cover letters based on resume and job description.
"""

from backend.data.block import Block, BlockCategory, BlockOutput, BlockSchema
from backend.data.model import SchemaField


class CoverLetterGeneratorBlock(Block):
    """
    Generates a customized cover letter based on the applicant's resume
    and the job description.
    """

    class Input(BlockSchema):
        applicant_name: str = SchemaField(
            description="Name of the applicant"
        )
        applicant_email: str = SchemaField(
            description="Email of the applicant",
            default=""
        )
        applicant_phone: str = SchemaField(
            description="Phone number of the applicant",
            default=""
        )
        resume_summary: str = SchemaField(
            description="Summary or key highlights from the resume"
        )
        job_title: str = SchemaField(
            description="Job title being applied for"
        )
        company_name: str = SchemaField(
            description="Name of the company"
        )
        job_description: str = SchemaField(
            description="Job description or key requirements"
        )
        tone: str = SchemaField(
            description="Tone of the cover letter (professional, enthusiastic, formal)",
            default="professional"
        )

    class Output(BlockSchema):
        cover_letter: str = SchemaField(
            description="Generated cover letter text"
        )
        subject_line: str = SchemaField(
            description="Suggested email subject line"
        )

    def __init__(self):
        super().__init__(
            id="d4e5f6g7-8901-23de-f456-4567890123de",
            description="Generates customized cover letters based on resume information and job descriptions",
            categories={BlockCategory.TEXT, BlockCategory.AI},
            input_schema=CoverLetterGeneratorBlock.Input,
            output_schema=CoverLetterGeneratorBlock.Output,
            test_input={
                "applicant_name": "John Doe",
                "applicant_email": "john.doe@example.com",
                "resume_summary": "Experienced software engineer with 5 years in web development",
                "job_title": "Senior Software Engineer",
                "company_name": "Tech Corp",
                "job_description": "Looking for a senior developer with Python and React experience",
                "tone": "professional"
            },
            test_output=[
                ("cover_letter", str),
                ("subject_line", str),
            ],
        )

    def run(self, input_data: Input, **kwargs) -> BlockOutput:
        """
        Generate a cover letter based on the provided information.
        """
        
        # Generate subject line
        subject_line = f"Application for {input_data.job_title} Position at {input_data.company_name}"
        
        # Build cover letter
        cover_letter_parts = []
        
        # Header with contact info
        if input_data.applicant_email or input_data.applicant_phone:
            header = f"{input_data.applicant_name}\n"
            if input_data.applicant_email:
                header += f"{input_data.applicant_email}\n"
            if input_data.applicant_phone:
                header += f"{input_data.applicant_phone}\n"
            cover_letter_parts.append(header)
        else:
            cover_letter_parts.append(f"{input_data.applicant_name}\n")
        
        # Date
        cover_letter_parts.append("\nDate: [Current Date]\n")
        
        # Company info
        cover_letter_parts.append(f"\n{input_data.company_name}")
        cover_letter_parts.append("Hiring Manager\n")
        
        # Salutation
        cover_letter_parts.append(f"\nDear Hiring Manager,\n")
        
        # Opening paragraph
        opening = (
            f"\nI am writing to express my strong interest in the {input_data.job_title} "
            f"position at {input_data.company_name}. "
        )
        
        if input_data.tone == "enthusiastic":
            opening += (
                "I am excited about the opportunity to contribute to your team and believe "
                "my experience and skills make me an excellent candidate for this role."
            )
        elif input_data.tone == "formal":
            opening += (
                "I believe my professional background and qualifications align well with "
                "the requirements outlined in your job posting."
            )
        else:  # professional
            opening += (
                "With my background and experience, I am confident I can make valuable "
                "contributions to your organization."
            )
        
        cover_letter_parts.append(opening)
        
        # Middle paragraph - highlight qualifications
        middle = (
            f"\n\n{input_data.resume_summary} "
            "My experience has equipped me with the skills and knowledge necessary to excel "
            f"in this role. "
        )
        
        # Add job description reference
        if input_data.job_description:
            middle += (
                "I have carefully reviewed the job description and am particularly drawn to "
                "the responsibilities and requirements outlined, which align well with my "
                "professional background."
            )
        
        cover_letter_parts.append(middle)
        
        # Closing paragraph
        closing = (
            "\n\nI am eager to bring my expertise to your team and contribute to "
            f"{input_data.company_name}'s continued success. I would welcome the opportunity "
            "to discuss how my skills and experience can benefit your organization. "
            "Thank you for considering my application. I look forward to hearing from you."
        )
        
        cover_letter_parts.append(closing)
        
        # Sign off
        cover_letter_parts.append("\n\nSincerely,")
        cover_letter_parts.append(f"\n{input_data.applicant_name}")
        
        # Combine all parts
        cover_letter = "".join(cover_letter_parts)
        
        yield "cover_letter", cover_letter
        yield "subject_line", subject_line
