# Additional Job Platform Integration Guide

This guide explains how to integrate additional job platforms beyond Adzuna.

## 🌐 Available Free/Accessible Job APIs

### 1. Adzuna ✅ (Currently Implemented)
- **Status**: Fully integrated
- **Cost**: Free forever
- **Coverage**: UAE, US, UK, CA, AU, IN, SG
- **Setup**: https://developer.adzuna.com/

### 2. The Muse API 🟡 (Easy to Add)
- **Cost**: Free tier available
- **Coverage**: Global
- **Docs**: https://www.themuse.com/developers/api/v2
- **Good for**: Company culture, editorial content

**Integration Steps:**
1. Register at https://www.themuse.com/developers
2. Get API key
3. Add to `RealJobSearchBlock` as new platform option

**Example API Call:**
```python
url = "https://www.themuse.com/api/public/jobs"
params = {
    "api_key": "your_key",
    "category": "Engineering",
    "location": "Dubai",
    "page": 1
}
response = requests.get(url, params=params)
```

### 3. JSearch (RapidAPI) 🟡 (Good Coverage)
- **Cost**: Free tier: 100 searches/month
- **Coverage**: Indeed, LinkedIn, Glassdoor aggregation
- **Docs**: https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch
- **Good for**: Multi-platform aggregation

**Integration Steps:**
1. Sign up at https://rapidapi.com/
2. Subscribe to JSearch (free tier)
3. Get RapidAPI key

**Example API Call:**
```python
import requests

url = "https://jsearch.p.rapidapi.com/search"
headers = {
    "X-RapidAPI-Key": "your_rapidapi_key",
    "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
}
params = {
    "query": "accountant in Dubai",
    "page": "1",
    "num_pages": "1"
}
response = requests.get(url, headers=headers, params=params)
```

### 4. LinkedIn Jobs 🔴 (Difficult)
- **Official API**: Requires LinkedIn Partner Program (not free/accessible)
- **Alternative 1**: LinkedIn RSS feeds (limited)
- **Alternative 2**: Proxycurl API (paid, but has free tier)

**Option A: RSS Feeds (Limited but Free)**
```python
import feedparser

def get_linkedin_jobs_rss(keywords, location):
    # LinkedIn job search RSS feed
    query = f"{keywords} {location}".replace(" ", "%20")
    url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={query}"
    
    # Note: This returns HTML, not RSS, so you'd need to parse it
    # or use LinkedIn's job widgets which are publicly accessible
```

**Option B: Proxycurl (Paid API with Free Trial)**
- Get API key: https://nubela.co/proxycurl/
- Free tier: Limited credits
- Docs: https://nubela.co/proxycurl/docs

### 5. Indeed API 🟡 (Limited but Free)
- **Publisher API**: Free but limited features
- **Docs**: https://opensource.indeedeng.io/api-documentation/
- **Good for**: Basic job search

**Integration Steps:**
1. Register at https://secure.indeed.com/account/register
2. Get Publisher ID from https://www.indeed.com/publisher
3. Add to `RealJobSearchBlock`

**Example API Call:**
```python
url = "https://api.indeed.com/ads/apisearch"
params = {
    "publisher": "your_publisher_id",
    "q": "accountant",  # query
    "l": "Dubai, UAE",  # location
    "format": "json",
    "v": "2",
    "limit": 25
}
response = requests.get(url, params=params)
```

**Note**: Indeed's Publisher API has limitations:
- Basic search only
- Limited to search results (not full job details)
- Can't apply through API

### 6. Gulf Talent 🔴 (No Public API)
- **Status**: No official API
- **Alternative**: Web scraping (check their terms)
- **Better option**: Contact them for partnership/API access

**If you want to scrape (get permission first!):**
```python
# Example using BeautifulSoup (requires permission)
# DO NOT use without Gulf Talent's permission
import requests
from bs4 import BeautifulSoup

url = "https://www.gulftalent.com/jobs/accountant-dubai"
# Add appropriate headers, rate limiting, and respect robots.txt
```

**Recommended**: Contact Gulf Talent business team for API access or partnership.

### 7. Remote Job Boards (Good for Remote Work)

**RemoteOK**
- API: https://remoteok.com/api
- Free and open
- No authentication required!

```python
response = requests.get("https://remoteok.com/api")
jobs = response.json()
```

**We Work Remotely**
- RSS Feeds available
- Categories for different job types

**Remote.co**
- Web scraping possible
- Check robots.txt and terms

## 🛠️ Implementation Template

To add a new job platform to `RealJobSearchBlock`:

```python
# In real_job_search.py

def _search_new_platform(
    self,
    api_key: str,
    query: str,
    location: str,
    **kwargs
) -> tuple[list[dict], int, str]:
    """
    Search jobs using NewPlatform API.
    """
    
    # 1. Build API URL
    url = "https://api.newplatform.com/jobs"
    
    # 2. Build parameters
    params = {
        "api_key": api_key,
        "q": query,
        "location": location,
        "limit": kwargs.get("limit", 20)
    }
    
    # 3. Make API request
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # 4. Parse results into standard format
        jobs = []
        for item in data.get("results", []):
            job = {
                "id": str(item.get("id")),
                "title": item.get("title"),
                "company": item.get("company"),
                "location": item.get("location"),
                "description": item.get("description"),
                "url": item.get("url"),
                "platform": "newplatform"
            }
            jobs.append(job)
        
        # 5. Return standardized data
        total = data.get("total", len(jobs))
        summary = f"Found {total} jobs via NewPlatform"
        
        return jobs, total, summary
        
    except Exception as e:
        raise RuntimeError(f"NewPlatform API error: {str(e)}")
```

Then add to the main run method:
```python
if input_data.platform == "newplatform":
    jobs, total, summary = self._search_new_platform(...)
```

## 📊 Platform Comparison

| Platform | Cost | Coverage | Ease | Quality | UAE Focus |
|----------|------|----------|------|---------|-----------|
| Adzuna | Free | Global | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| JSearch | Free tier | Multi | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Indeed | Free | Global | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| The Muse | Free tier | Global | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| LinkedIn | Paid/Hard | Global | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Gulf Talent | No API | UAE | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| RemoteOK | Free | Remote | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | N/A |

## 🎯 Recommended Strategy

### For UAE Job Hunting (Your Use Case):

**Tier 1: Start Here (Free & Easy)**
1. ✅ **Adzuna** - Already implemented
2. 🟡 **Indeed Publisher API** - Add next
3. 🟡 **JSearch** - Aggregates multiple sources

**Tier 2: More Options (Requires Work)**
1. 🟡 **The Muse** - Good for company culture info
2. 🟡 **RemoteOK** - If open to remote work
3. 🔴 **LinkedIn RSS** - Limited but better than nothing

**Tier 3: Contact/Partnership Required**
1. 🔴 **Gulf Talent** - Best UAE jobs but no public API
2. 🔴 **Bayt.com** - Major UAE platform, contact for API
3. 🔴 **Naukri Gulf** - Another major UAE platform

## 🚀 Quick Wins

### 1. Add Indeed (30 minutes)
```python
# Get publisher ID from Indeed
# Add method to RealJobSearchBlock
# Test with UAE locations
```

### 2. Add JSearch via RapidAPI (20 minutes)
```python
# Sign up for RapidAPI
# Get free tier access
# Integrate JSearch endpoint
```

### 3. Add RemoteOK (15 minutes)
```python
# No auth needed!
# Just parse their JSON API
# Filter by skills/keywords
```

## 📝 Testing New Integrations

Template for testing new platforms:

```python
# test_new_platform.py
import requests

def test_api_connection():
    """Test basic API connectivity"""
    url = "https://api.platform.com/test"
    response = requests.get(url)
    assert response.status_code == 200
    print("✓ API connection works")

def test_job_search():
    """Test job search functionality"""
    url = "https://api.platform.com/jobs"
    params = {"q": "test", "location": "Dubai"}
    response = requests.get(url, params=params)
    data = response.json()
    
    assert "results" in data or "jobs" in data
    print(f"✓ Found {len(data.get('results', []))} jobs")

def test_rate_limits():
    """Test API rate limits"""
    for i in range(5):
        response = requests.get("https://api.platform.com/jobs")
        print(f"Request {i+1}: {response.status_code}")
        time.sleep(1)
    print("✓ Rate limits OK")

if __name__ == "__main__":
    test_api_connection()
    test_job_search()
    test_rate_limits()
```

## 🔐 API Key Management

Store API keys securely in `.env`:

```bash
# .env file
ADZUNA_APP_ID=your_app_id
ADZUNA_APP_KEY=your_app_key
INDEED_PUBLISHER_ID=your_publisher_id
JSEARCH_RAPIDAPI_KEY=your_rapidapi_key
THEMUSE_API_KEY=your_muse_key
```

Access in code:
```python
import os
from dotenv import load_dotenv

load_dotenv()

app_id = os.getenv("ADZUNA_APP_ID")
app_key = os.getenv("ADZUNA_APP_KEY")
```

## 📞 Contact Information for Partnerships

If you want official API access:

**Gulf Talent**
- Website: https://www.gulftalent.com/
- Contact: business@gulftalent.com
- Mention: API access for job search integration

**Bayt.com**
- Website: https://www.bayt.com/
- Contact: Through their business inquiry form
- Mention: API integration for career services

**Naukri Gulf**
- Website: https://www.naukrigulf.com/
- Part of Naukri.com (Info Edge India)
- Contact through corporate website

## 🎓 Next Steps

1. **Try Quick Wins**: Add Indeed and RemoteOK first
2. **Test Integration**: Verify APIs work with UAE locations
3. **Monitor Usage**: Track API limits and costs
4. **Contact Platforms**: Reach out to Gulf Talent for partnership
5. **Optimize**: Cache results, deduplicate across platforms

## 💡 Pro Tips

1. **Aggregate Results**: Merge jobs from multiple platforms
2. **Deduplicate**: Same job may appear on multiple platforms
3. **Cache Results**: Don't fetch same jobs repeatedly
4. **Respect Rate Limits**: Be a good API citizen
5. **Error Handling**: One platform failing shouldn't break workflow

## 📚 Resources

- **API List**: https://github.com/public-apis/public-apis (search "Jobs")
- **RapidAPI Hub**: https://rapidapi.com/search/jobs
- **Job Board List**: https://www.jobboardfinder.com/
- **UAE Specific**: Focus on Middle East job boards

---

**Need help integrating a specific platform? Check the AutoGPT Discord community!**
