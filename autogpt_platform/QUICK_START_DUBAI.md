# 🚀 Quick Start - For Dubai Job Seekers

## ⚡ 3-Step Setup (5 Minutes)

### Step 1: Start the Platform
```bash
cd autogpt_platform
docker compose up -d
```
⏱️ Wait 2-3 minutes for services to start

### Step 2: Get Indeed Publisher ID
1. Go to: **https://www.indeed.com/publisher**
2. Sign in with your Indeed account
3. Click "Register" → Fill basic info
4. Copy your Publisher ID (number like: 1234567890)

### Step 3: Connect & Search
1. Open: **http://localhost:3000/job-hunt**
2. Click **"Platforms"** tab
3. Paste Publisher ID in **Indeed** section
4. Click **"Connect"**

**✅ Ready to search for jobs in Dubai!**

---

## 📱 Using the Dashboard

### Add Your Resume (Profile Tab)
- Paste your resume text OR
- Upload .txt file
- Click "Save Profile"

### Search for Jobs (Job Search Tab)
Add what you want:
- **Job Titles**: Cashier, Accountant, Sales Associate
- **Locations**: Dubai UAE, Abu Dhabi UAE
- **Keywords**: customer service, cash handling, QuickBooks

Click **"Search for Jobs"**

### View Results
- Jobs appear with **match scores** (0-100%)
- Higher score = better match
- Click "View & Apply" to see details

### Track Applications (Applications Tab)
- See all your applications
- Monitor status (pending, applied, interviewing)
- Check statistics

---

## 🆘 Quick Fixes

### Can't access dashboard?
```bash
# Check if running:
docker compose ps

# If not running, start:
docker compose up -d

# Wait 2-3 minutes, then try:
# http://localhost:3000/job-hunt
```

### Need Docker?
- **Mac/Windows**: Install Docker Desktop
- **Linux**: `sudo apt install docker.io docker-compose`

### Publisher ID not working?
- Make sure you copied the full number
- No spaces before/after
- Try the number that looks like: 1234567890

---

## 💡 Dubai Job Search Tips

**Best Job Titles:**
- Cashier
- Sales Associate  
- Accountant
- Retail Assistant
- Customer Service

**Best Locations:**
- Dubai, UAE
- Abu Dhabi, UAE
- Just "Dubai" (simpler works better)

**Good Keywords:**
- cash handling
- customer service
- POS systems
- QuickBooks (for accounting)
- Excel

---

## 📚 More Help

- **Troubleshooting**: `JOB_HUNT_TROUBLESHOOTING.md`
- **Complete Guide**: `JOB_HUNT_DASHBOARD_GUIDE.md`
- **Quick Start**: `JOB_HUNT_DASHBOARD_README.md`

---

## ✅ Checklist

Before you start:
- [ ] Docker installed and running
- [ ] Platform started (`docker compose up -d`)
- [ ] Dashboard opens at http://localhost:3000/job-hunt
- [ ] Indeed Publisher ID obtained
- [ ] Indeed connected (green badge)
- [ ] Resume uploaded
- [ ] Job preferences set

**All checked?** Start searching! 🎉

---

**Need help?** Check `JOB_HUNT_TROUBLESHOOTING.md` or ask on Discord!

**Good luck with your Dubai job search!** 🚀🇦🇪
