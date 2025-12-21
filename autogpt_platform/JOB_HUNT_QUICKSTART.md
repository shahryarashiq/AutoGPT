# Job Hunt Automation - Quick Start Guide

## 🎯 What This Does

This automation system helps you:
- **Search** for jobs across multiple platforms (UAE focus: Dubai, Abu Dhabi, etc.)
- **Optimize** your resume for each job (keyword matching for ATS systems)
- **Generate** customized cover letters automatically
- **Track** all your applications in one place

**100% FREE** - No subscriptions needed! Uses free APIs and runs on your machine.

## 🚀 Quick Setup (5 Minutes)

### Step 1: Start AutoGPT Platform

```bash
# If not already running
cd autogpt_platform
docker compose up -d
```

Wait a few minutes for all services to start, then open http://localhost:3000

### Step 2: Get Free API Access (Optional but Recommended)

For real job searches, get free Adzuna API credentials:

1. Go to https://developer.adzuna.com/
2. Click "Sign Up" (free, no credit card)
3. Create an application
4. Copy your:
   - **Application ID**
   - **Application Key**

Save these - you'll need them in Step 4!

### Step 3: Load the Job Hunt Template

1. Open AutoGPT at http://localhost:3000
2. Click "Create New Agent" or "Templates"
3. Look for **"Job Hunt Automation"** template
4. Click to load it

### Step 4: Configure Your Job Search

Edit the blocks in the workflow:

#### A. Resume Parser Block
```
Paste your resume text here, or upload a file
```

#### B. Job Search Block (Choose One)

**Option 1: Real Jobs (Adzuna - Free API)**
- Block: `RealJobSearchBlock`
- Enter your Adzuna credentials from Step 2
- Set your search:
  - Query: "cashier" or "accountant" 
  - Location: "Dubai" or "Abu Dhabi"
  - Country: "ae" (for UAE)

**Option 2: Mock Jobs (For Testing)**
- Block: `JobSearchBlock`
- Set job titles: ["Cashier", "Accountant"]
- Set locations: ["Dubai, UAE", "Abu Dhabi, UAE"]

#### C. Resume Optimizer
```
auto_add_keywords: true
```

#### D. Cover Letter Generator
```
tone: "professional"
```

### Step 5: Run Your Job Hunt!

1. Click **"Run"** button
2. Watch the automation:
   - ✅ Parse your resume
   - ✅ Search for jobs
   - ✅ Optimize resume for each job
   - ✅ Generate cover letters
   - ✅ Track applications

3. View results in the output panels

## 📊 Understanding Your Results

### Resume Parser Output
- Contact info extracted
- Skills identified
- Keywords found

### Job Search Output
- List of matching jobs
- Company names
- Locations
- Job descriptions
- Direct application links

### Resume Optimizer Output
- **Match Score**: How well your resume matches (aim for 70%+)
- **Missing Keywords**: Add these to your resume
- **Suggestions**: Tips to improve your match

### Cover Letter Output
- Customized letter for each position
- Professional formatting
- Email subject line

### Application Tracker
- All applications recorded
- Status tracking
- Statistics dashboard

## 🎨 Customization Tips

### Job Titles (Multiple Positions)
```json
"job_titles": [
  "Cashier",
  "Retail Sales Associate", 
  "Store Clerk",
  "Accountant",
  "Accounts Assistant"
]
```

### Locations (Multiple Cities)
```json
"locations": [
  "Dubai, UAE",
  "Abu Dhabi, UAE",
  "Sharjah, UAE",
  "Ajman, UAE"
]
```

### Keywords (Your Skills)
```json
"keywords": [
  "customer service",
  "cash handling",
  "POS systems",
  "QuickBooks",
  "Excel"
]
```

## 💡 Pro Tips

### 1. Start with Mock Data
Use `JobSearchBlock` first to test your workflow without API limits.

### 2. Review Before Sending
The automation helps you apply faster, but ALWAYS:
- Review the optimized resume
- Personalize the cover letter
- Check the company website
- Verify you meet requirements

### 3. Track Everything
Use the Application Tracker to:
- Record application dates
- Set follow-up reminders
- Track interview stages
- Measure success rate

### 4. Optimize Your Resume
If match scores are low (<50%):
- Add relevant skills section
- Include keywords from job postings
- Highlight relevant experience
- Consider online courses for missing skills

### 5. Be Honest
- Only add keywords for skills you actually have
- Don't lie about experience
- Personalize each application
- Follow up professionally

## 🌍 Supported Countries (Adzuna)

Current support for real job searches:
- 🇦🇪 **UAE** (Dubai, Abu Dhabi, etc.) - Code: `ae`
- 🇺🇸 **United States** - Code: `us`
- 🇬🇧 **United Kingdom** - Code: `uk`
- 🇨🇦 **Canada** - Code: `ca`
- 🇦🇺 **Australia** - Code: `au`
- 🇮🇳 **India** - Code: `in`
- 🇸🇬 **Singapore** - Code: `sg`

## 🔧 Troubleshooting

### "No jobs found"
- Try broader keywords
- Expand location search
- Check country code is correct
- Verify API credentials

### "Low match score"
- Add more relevant skills to resume
- Include job-specific keywords
- Enable `auto_add_keywords`

### "API error"
- Check your Adzuna credentials
- Verify internet connection
- Check API rate limits

### "Blocks not showing"
- Restart the platform
- Check Docker services: `docker compose ps`
- View logs: `docker compose logs`

## 📚 Need More Help?

- **Full Guide**: See `/autogpt_platform/JOB_HUNT_GUIDE.md`
- **Block Details**: See `/autogpt_platform/backend/backend/blocks/job_hunt/README.md`
- **AutoGPT Docs**: https://docs.agpt.co
- **Discord**: https://discord.gg/autogpt

## 🎓 Next Steps

Once you're comfortable:

1. **Schedule Runs**: Set workflow to run daily
2. **Add Email**: Integrate email sending for applications
3. **Multiple Platforms**: Add more job sources
4. **Follow-ups**: Create reminder workflows
5. **Interview Prep**: Build interview question generators

## 💰 Cost Breakdown

| Component | Cost |
|-----------|------|
| AutoGPT Platform | **FREE** (self-hosted) |
| Adzuna API | **FREE** (forever) |
| Other Job APIs | **FREE** (most have free tiers) |
| Your Computer | Just electricity! |
| **TOTAL** | **$0/month** 🎉 |

## ⚠️ Important Notes

### Legal & Ethical
- Use responsibly
- Follow platform terms of service
- Don't spam applications
- Personalize before sending
- Be honest in applications

### Privacy
- All data stays on your machine
- No data sent to third parties (except job platform APIs)
- Your resume is private
- No tracking or analytics

### Quality Over Quantity
This tool helps you apply faster, but remember:
- Quality applications > Mass applications
- Personalize each cover letter
- Research companies
- Apply only where you're qualified

---

## 🎯 Ready to Start?

1. ✅ Platform running at http://localhost:3000
2. ✅ API credentials ready (optional)
3. ✅ Resume prepared
4. ✅ Job preferences decided

**Go to Step 3 and load the template!**

---

**Good luck with your job hunt! 🚀**

*Remember: This is a tool to help you, not replace your effort. The best applications are personalized and thoughtful.*
