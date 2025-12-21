# Job Hunt Dashboard - User Guide

## 🎉 Your Dashboard is Ready!

The Job Hunt Automation dashboard is now available in your AutoGPT platform.

## 🚀 How to Access

1. **Start the AutoGPT Platform** (if not already running):
   ```bash
   cd autogpt_platform
   docker compose up -d
   ```

2. **Open your browser** and navigate to:
   ```
   http://localhost:3000/job-hunt
   ```

3. **Login** to your AutoGPT account if required

## 📱 Dashboard Sections

### 1. Profile & Resume Tab

**What to do:**
- Click the "Profile & Resume" tab
- Enter your name, email, and phone number
- Paste your resume text in the text area OR click "Upload Resume" to upload a .txt file
- Click "Save Profile"

**What happens:**
- Your information is saved locally
- The system automatically extracts skills and keywords from your resume
- You'll see a "Parsed Resume Data" section showing what was found

### 2. Job Search Tab

**What to do:**
- Click the "Job Search" tab
- Add job titles you're looking for:
  - Type "Cashier" and click the + button
  - Type "Accountant" and click the + button
  - Add as many as you want!
- Add locations:
  - Type "Dubai, UAE" and click +
  - Type "Abu Dhabi, UAE" and click +
- Add keywords (optional):
  - Type "customer service" and click +
  - Type "QuickBooks" and click +
- Click "Search for Jobs" button

**What happens:**
- The system searches for matching jobs
- Results appear below with match scores
- Each job shows title, company, location, salary
- Higher match scores mean better fit for your resume

### 3. Platforms Tab

**What to do:**
- Click the "Platforms" tab
- For Adzuna (recommended - it's FREE!):
  1. Click "Get API Key" button
  2. Sign up at https://developer.adzuna.com/
  3. Create an application (takes 2 minutes)
  4. Copy your Application ID and Application Key
  5. Paste them in the dashboard
  6. Click "Connect"

**What happens:**
- Your credentials are saved securely
- The platform shows "Connected" status
- You can now use Adzuna for real job searches

**Other Platforms:**
- Indeed: Follow similar process at indeed.com/publisher
- LinkedIn: Requires partner access (not free)
- Gulf Talent: Contact them for API access

### 4. Applications Tab

**What to do:**
- Click the "Applications" tab
- View all your job applications
- See statistics:
  - Total applications
  - Applied count
  - Interviewing count
  - Average match score

**What happens:**
- See all jobs you've applied to
- Track status of each application
- Monitor your progress
- Update application status as you get responses

## 💡 Tips for Best Results

### Resume Tips:
1. **Keep it text-based**: The parser works best with plain text
2. **Include keywords**: Add skills like "QuickBooks", "Excel", "customer service"
3. **Be specific**: Mention job titles you've held

### Search Tips:
1. **Start broad**: Add multiple job titles
2. **Multiple locations**: Cast a wider net
3. **Use keywords**: Skills and requirements you have
4. **Check match scores**: Focus on jobs with 70%+ match

### Platform Tips:
1. **Start with Adzuna**: It's completely free and works great for UAE
2. **Get API keys early**: Takes 5 minutes, saves time later
3. **Keep credentials safe**: They're stored locally in your browser

## 🎯 Example Workflow

**Day 1 - Setup:**
1. Add your resume (5 minutes)
2. Get Adzuna API key (5 minutes)
3. Connect Adzuna (1 minute)
4. Configure job preferences (3 minutes)

**Day 2+ - Job Hunting:**
1. Click "Search for Jobs" daily
2. Review new matches
3. Apply to jobs with high match scores
4. Track applications in Applications tab
5. Update statuses as you get responses

## 📊 Understanding Match Scores

- **80-100%**: Excellent match - Apply immediately!
- **60-79%**: Good match - Review and consider
- **40-59%**: Fair match - May need to adapt resume
- **0-39%**: Low match - Probably not a good fit

## ⚙️ Advanced Features (Coming Soon)

The current dashboard uses localStorage for demo purposes. Future updates will:
- Connect directly to backend blocks
- Auto-generate cover letters
- Auto-optimize resumes per job
- Send applications automatically
- Email notifications
- Interview scheduling

## 🆘 Troubleshooting

### "Can't access /job-hunt page"
- Make sure AutoGPT platform is running
- Check you're logged in
- Try: http://localhost:3000/job-hunt

### "Search not working"
- Connect Adzuna first (or use mock data)
- Check API credentials are correct
- Verify internet connection

### "Resume not parsing correctly"
- Use plain text format
- Remove special characters
- Make sure resume has clear sections (Skills, Experience, etc.)

### "API connection failed"
- Double-check API keys
- Verify keys are active on platform website
- Try disconnecting and reconnecting

## 📚 Related Documentation

- Full Guide: `/autogpt_platform/JOB_HUNT_GUIDE.md`
- Quick Start: `/autogpt_platform/JOB_HUNT_QUICKSTART.md`
- Platform Integration: `/autogpt_platform/JOB_PLATFORM_INTEGRATION.md`

## 🎉 You're All Set!

Your job hunt automation dashboard is ready to use. Start by:
1. Going to http://localhost:3000/job-hunt
2. Adding your resume
3. Connecting Adzuna (5 minutes to get API key)
4. Searching for jobs!

**Good luck with your job hunt! 🚀**

---

Need help? Check the documentation files or ask in the AutoGPT Discord: https://discord.gg/autogpt
