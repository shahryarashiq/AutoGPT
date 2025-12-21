# Job Hunt Dashboard - Troubleshooting & Setup

## 🚨 Issue: Can't Access Dashboard (ERR_CONNECTION_REFUSED)

If you see "ERR_CONNECTION_REFUSED" when trying to access `http://localhost:3000/job-hunt`, follow these steps:

### Step 1: Check if AutoGPT Platform is Running

```bash
cd /path/to/AutoGPT/autogpt_platform
docker compose ps
```

If you see services are not running, start them:

```bash
docker compose up -d
```

Wait 2-3 minutes for all services to start, then try accessing the dashboard again.

### Step 2: Check Docker Status

Make sure Docker is running:

```bash
docker ps
```

If you get an error, start Docker Desktop (on Mac/Windows) or Docker service (on Linux):

**Mac/Windows:**
- Open Docker Desktop application
- Wait for it to show "Docker Desktop is running"

**Linux:**
```bash
sudo systemctl start docker
```

### Step 3: Verify Port 3000 is Available

Check if another service is using port 3000:

**Mac/Linux:**
```bash
lsof -i :3000
```

**Windows:**
```bash
netstat -ano | findstr :3000
```

If port 3000 is in use, either:
- Stop the other service
- Or modify the docker-compose.yml to use a different port

### Step 4: Check Logs for Errors

```bash
cd /path/to/AutoGPT/autogpt_platform
docker compose logs frontend
```

Look for any error messages and address them.

### Step 5: Restart Everything

If still not working:

```bash
cd /path/to/AutoGPT/autogpt_platform
docker compose down
docker compose up -d
```

Wait 2-3 minutes, then try: `http://localhost:3000/job-hunt`

---

## ✅ How to Get Indeed Publisher ID (FREE - 2 Minutes)

Since you already have an Indeed account, this is super easy!

### Step 1: Go to Indeed Publisher Portal

Open: **https://www.indeed.com/publisher**

### Step 2: Sign In

- Click "Sign In" or "Register"
- Use your existing Indeed account credentials
- If you don't have an account yet, create one (free)

### Step 3: Register as Publisher

1. Fill in basic information:
   - Your name
   - Email (use your existing Indeed email)
   - Website (you can use a placeholder like "http://localhost:3000")
   - Purpose: "Job Board" or "Personal Use"

2. Agree to terms and conditions

3. Click "Register" or "Submit"

### Step 4: Get Your Publisher ID

After registration:
- You'll see your **Publisher ID** on the dashboard
- It looks like a number: `1234567890`
- Copy this number

### Step 5: Connect in Dashboard

1. Go to: `http://localhost:3000/job-hunt`
2. Click "Platforms" tab
3. Find "Indeed" section
4. Paste your Publisher ID
5. Click "Connect"

**Done!** ✅ You can now search for jobs using Indeed API.

---

## 🎯 Quick Start After Setup

Once dashboard is accessible and Indeed is connected:

1. **Profile Tab**
   - Upload your resume (text file) or paste it
   - Click "Save Profile"

2. **Job Search Tab**
   - Add job titles: "Cashier", "Accountant", etc.
   - Add locations: "Dubai, UAE", "Abu Dhabi, UAE"
   - Click "Search for Jobs"

3. **View Results**
   - See jobs with match scores
   - Apply to jobs with high scores

4. **Applications Tab**
   - Track all your applications
   - Monitor progress

---

## 📝 Alternative: Using Mock Data (No API Needed)

If you can't get API keys immediately, you can still test the dashboard with mock data:

1. Go to: `http://localhost:3000/job-hunt`
2. Skip the "Platforms" tab
3. Go to "Job Search" tab
4. Configure your preferences
5. Click "Search for Jobs"

The system will show **demo jobs** for testing. This lets you:
- Test the interface
- See how it works
- Prepare your resume
- Configure preferences

Once you get Indeed Publisher ID, you'll get real jobs!

---

## 🔧 Common Issues & Solutions

### "Publisher ID not working"

**Solution:**
- Make sure you copied the full number
- No spaces before/after
- Try disconnecting and reconnecting
- Check you're using the correct Publisher ID (not API key)

### "No jobs found"

**Solution:**
- Try broader search terms
- Check location is correct: "Dubai" not "Dubai, United Arab Emirates"
- Try different job titles
- Make sure Indeed is connected (green "Connected" badge)

### "Dashboard is slow"

**Solution:**
- Check your internet connection
- Restart Docker containers
- Clear browser cache
- Try a different browser

### "Can't save profile"

**Solution:**
- Check browser console for errors (F12 > Console)
- Try clearing browser localStorage
- Refresh the page and try again

---

## 💡 Tips for Dubai Job Hunting

### Best Job Titles to Search:
- "Cashier"
- "Sales Associate"
- "Retail Assistant"
- "Accountant"
- "Accounts Assistant"
- "Customer Service"
- "Store Keeper"

### Best Locations:
- "Dubai, UAE"
- "Abu Dhabi, UAE"
- "Sharjah, UAE"
- Just "Dubai" (simpler often works better)

### Keywords to Add:
- "cash handling"
- "customer service"
- "retail"
- "POS"
- "QuickBooks" (for accounting)
- "Excel"

---

## 🆘 Still Need Help?

### Check Documentation:
- `JOB_HUNT_DASHBOARD_README.md` - Quick start
- `JOB_HUNT_DASHBOARD_GUIDE.md` - Complete guide
- `JOB_HUNT_GUIDE.md` - Detailed feature docs

### Contact Support:
- AutoGPT Discord: https://discord.gg/autogpt
- GitHub Issues: Create issue with 'job-hunt' label

### Provide These Details:
1. Operating System (Windows/Mac/Linux)
2. Docker version: `docker --version`
3. Error message (full text)
4. What you tried already
5. Screenshot if possible

---

## ✅ Success Checklist

Before starting your job hunt, make sure:

- [ ] Docker is running
- [ ] AutoGPT platform is started (`docker compose up -d`)
- [ ] Dashboard accessible at `http://localhost:3000/job-hunt`
- [ ] Indeed Publisher ID obtained (2 minutes)
- [ ] Indeed connected in Platforms tab
- [ ] Resume uploaded in Profile tab
- [ ] Job preferences configured
- [ ] Test search shows results

**Ready!** You can now start applying for jobs automatically! 🎉

---

**Good luck with your job search in Dubai!** 🚀
