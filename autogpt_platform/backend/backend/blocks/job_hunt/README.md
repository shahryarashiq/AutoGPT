# Job Hunt Automation Blocks

This package provides a comprehensive set of blocks for automating job search and application processes on the AutoGPT platform.

## Blocks Overview

### 1. ResumeParserBlock
**ID:** `a1b2c3d4-5678-90ab-cdef-1234567890ab`

Parses resume text and extracts structured information.

**Inputs:**
- `resume_text` (string): The text content of the resume to parse

**Outputs:**
- `name` (string): Extracted name
- `email` (string): Extracted email address
- `phone` (string): Extracted phone number
- `skills` (list): List of extracted skills
- `experience` (string): Work experience section
- `education` (string): Education section
- `summary` (string): Professional summary
- `keywords` (list): Extracted keywords

### 2. JobSearchBlock
**ID:** `b2c3d4e5-6789-01bc-def2-2345678901bc`

Generic job search block with mock data for testing workflows.

**Inputs:**
- `platform` (string): Job platform (indeed, linkedin, gulftalent, generic)
- `job_titles` (list): Desired job titles
- `locations` (list): Desired locations
- `keywords` (list): Additional keywords
- `experience_level` (string): Desired experience level
- `max_results` (int): Maximum results to return

**Outputs:**
- `jobs` (list): List of job postings
- `total_found` (int): Total number of jobs found
- `search_summary` (string): Search summary

### 3. RealJobSearchBlock
**ID:** `g7h8i9j0-1234-56gh-7890-7890123456gh`

Real job search integration using Adzuna's free API.

**Inputs:**
- `platform` (string): Currently only "adzuna"
- `app_id` (string): Adzuna App ID (free from https://developer.adzuna.com/)
- `app_key` (string): Adzuna App Key
- `query` (string): Job search query
- `location` (string): Location to search
- `country_code` (string): Country code (ae, us, uk, ca, au, in, sg)
- `results_per_page` (int): Number of results (max 50)
- `page` (int): Page number for pagination
- `sort_by` (string): Sort method (default, date, salary)

**Outputs:**
- `jobs` (list): List of real job postings from Adzuna
- `total_results` (int): Total available results
- `search_summary` (string): Search summary
- `error` (string): Error message if any

### 4. ResumeOptimizerBlock
**ID:** `c3d4e5f6-7890-12cd-ef34-3456789012cd`

Optimizes resumes by matching keywords with job descriptions.

**Inputs:**
- `resume_text` (string): Current resume text
- `job_description` (string): Job description to optimize for
- `auto_add_keywords` (bool): Whether to automatically add missing keywords

**Outputs:**
- `optimized_resume` (string): Resume with added keywords
- `missing_keywords` (list): Keywords missing from original resume
- `matching_keywords` (list): Keywords already present
- `optimization_suggestions` (string): Suggestions for improvement
- `match_score` (float): Match percentage (0-100)

### 5. CoverLetterGeneratorBlock
**ID:** `d4e5f6g7-8901-23de-f456-4567890123de`

Generates customized cover letters.

**Inputs:**
- `applicant_name` (string): Applicant's name
- `applicant_email` (string): Applicant's email
- `applicant_phone` (string): Applicant's phone
- `resume_summary` (string): Resume highlights
- `job_title` (string): Job title
- `company_name` (string): Company name
- `job_description` (string): Job description
- `tone` (string): Letter tone (professional, enthusiastic, formal)

**Outputs:**
- `cover_letter` (string): Generated cover letter
- `subject_line` (string): Email subject line

### 6. JobApplicationTrackerBlock
**ID:** `e5f6g7h8-9012-34ef-5678-5678901234ef`

Tracks job applications with status management.

**Inputs:**
- `action` (string): Action to perform (add, update, get, list_all)
- `job_id` (string): Unique job identifier
- `job_title` (string): Job title
- `company_name` (string): Company name
- `location` (string): Job location
- `platform` (string): Platform where job was found
- `job_url` (string): URL to job posting
- `status` (string): Application status
- `notes` (string): Additional notes
- `salary_range` (string): Salary information

**Outputs:**
- `success` (bool): Operation success status
- `message` (string): Status message
- `application_data` (dict): Single application data
- `all_applications` (list): All applications
- `statistics` (dict): Application statistics

## Usage Example

### Basic Workflow

1. **Parse Resume**
   ```
   ResumeParserBlock
   Input: Your resume text
   Output: Structured resume data
   ```

2. **Search Jobs**
   ```
   RealJobSearchBlock (for real jobs) or JobSearchBlock (for testing)
   Input: Job criteria
   Output: List of matching jobs
   ```

3. **Optimize Resume**
   ```
   ResumeOptimizerBlock
   Input: Resume + Job Description
   Output: Optimized resume with better keyword match
   ```

4. **Generate Cover Letter**
   ```
   CoverLetterGeneratorBlock
   Input: Resume info + Job details
   Output: Customized cover letter
   ```

5. **Track Application**
   ```
   JobApplicationTrackerBlock
   Input: Application details
   Output: Confirmation and statistics
   ```

## Getting Free API Access

### Adzuna (Recommended - Completely Free)

1. Visit https://developer.adzuna.com/
2. Sign up for a free account
3. Create an application to get:
   - Application ID
   - Application Key
4. Use these credentials in the RealJobSearchBlock

**Supported Countries:**
- UAE (ae) - Dubai, Abu Dhabi, etc.
- United States (us)
- United Kingdom (uk)
- Canada (ca)
- Australia (au)
- India (in)
- Singapore (sg)

### Rate Limits
- Free tier: Reasonable limits for personal use
- No cost: Completely free forever
- No credit card required

## Advanced Features

### Chaining Multiple Job Sources

Create multiple job search blocks and merge results:
1. RealJobSearchBlock (Adzuna)
2. JobSearchBlock (for other sources when you add them)
3. Merge and deduplicate results
4. Feed to Resume Optimizer

### Filtering and Prioritization

Add custom blocks to:
- Filter by salary range
- Prioritize by company rating
- Exclude specific companies
- Sort by posting date

### Automated Follow-ups

Create workflows for:
- Scheduling follow-up reminders
- Tracking interview stages
- Managing offer negotiations

## Testing

All blocks include test data and can be tested individually:

```python
from backend.blocks.job_hunt import ResumeParserBlock

block = ResumeParserBlock()
# Run with test data
for key, value in block.run(block.test_input[0]):
    print(f"{key}: {value}")
```

## Future Enhancements

Planned additions:
- [ ] LinkedIn integration (requires partner access)
- [ ] Indeed official API integration
- [ ] Email sending for applications
- [ ] Calendar integration for interviews
- [ ] Salary comparison tools
- [ ] Company research automation
- [ ] Interview question preparation
- [ ] Offer letter management

## Contributing

To add new job platform integrations:

1. Create a new method in RealJobSearchBlock
2. Add the platform to the Literal type
3. Implement the API integration
4. Update documentation
5. Add tests

## Support

For issues or questions:
- Check the main documentation: `/autogpt_platform/JOB_HUNT_GUIDE.md`
- AutoGPT Discord: https://discord.gg/autogpt
- GitHub Issues: Create an issue with the `job-hunt` label

## License

Part of the AutoGPT Platform - Polyform Shield License
