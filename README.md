# Marketing Engine - Free API Edition

A Streamlit web application that generates social media content from trending topics **without requiring any API keys or paid services**.

## 🚀 Features

✅ **Reddit Scraping** - Fetch trending posts from Reddit using `snscrape` or JSON API fallback
✅ **Twitter/X Scraping** - Extract tweets and engagement data using `snscrape`
✅ **YouTube Scraping** - Get video metadata using `yt-dlp`
✅ **Content Analysis** - Extract key themes from multiple sources
✅ **Social Media Post Generator** - Template-based post creation
✅ **Source Links** - Direct links to original content that inspired posts
✅ **AI Video Prompts** - Ready-to-use prompts for AI video generation tools
✅ **100% Free** - No API keys, no cost, no rate limit surprises

## 🛠️ Free Tools Used

### 1. **snscrape** - Social Network Scraper
- 🔗 **Use for:** Reddit posts, Twitter/X tweets
- **Why:** No authentication needed, works around API restrictions
- **Installation:** `pip install snscrape`

### 2. **yt-dlp** - YouTube Downloader
- 🔗 **Use for:** YouTube video metadata, transcripts
- **Why:** Powerful, maintained fork of youtube-dl
- **Installation:** `pip install yt-dlp`

### 3. **Beautiful Soup 4** - HTML Parser (Optional)
- **Use for:** Parsing custom web scraping
- **Installation:** `pip install beautifulsoup4`

---

## 📋 Installation & Setup

### Step 1: Clone/Download Project
```bash
cd "C:\Users\aksha\OneDrive\Desktop\projects\Marketing engine"
```

### Step 2: Create Virtual Environment (Recommended)
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the App
**Option 1: Double-click the batch file**
```bash
# Simply double-click run_app.bat in your project folder
```

**Option 2: Manual command**
```bash
cd "C:\Users\aksha\OneDrive\Desktop\projects\Marketing engine"
venv\Scripts\activate
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### AI Video Generation Prompts

Each generated social media post now includes a detailed AI video prompt that you can copy and paste into AI video generation tools like:

- **Runway ML** - Text-to-video generation
- **Pika Labs** - Fast video creation
- **Synthesia** - Professional avatar videos
- **HeyGen** - Business presentation videos
- **Descript** - Script-to-video conversion

The prompts include:
- The original post text
- Key themes from research
- Video specifications (duration, style, visuals)
- Script outline structure
- Professional branding guidelines

---

## 📝 How to Use

1. **Enter a Topic:** Type any industry, trend, or keyword (e.g., "AI Tools", "Fitness", "Web3")
2. **Select Data Sources:** Choose Reddit, Twitter/X, YouTube (or all three)
3. **Click "Generate Content":** The app scrapes data from selected sources
4. **View Results:** See collected data and AI-generated social media posts
5. **Check Sources:** Expand "Content Sources" to see links to original posts
6. **Get Video Prompts:** Click expanders under each post for AI video generation prompts
7. **Copy & Post:** Use generated posts on your social media accounts

---

## � Sharing This App With Friends

### Method 1: Share Project Folder (Easiest)
```bash
# Your friend needs to:
1. Unzip the project folder you send them
2. Install Python (if not installed) from python.org
3. Open terminal/command prompt in the project folder
4. Run: pip install -r requirements.txt
5. Run: streamlit run app.py
6. App opens at http://localhost:8501
```

### Method 2: Deploy to Streamlit Cloud (Free & No Installation Required)
```bash
# You do this, they just click a link:
1. Create a free GitHub account
2. Upload your project files to a new repository
3. Go to https://share.streamlit.io
4. Connect your GitHub and select the repository
5. Choose app.py as the main file
6. Click Deploy!
7. Share the generated URL (e.g., https://your-app-name.streamlit.app)
```

### Method 3: Railway Deployment (Free Tier)
```bash
1. Connect your GitHub repository
2. Railway auto-detects Python/Streamlit
3. Deploys automatically with a public URL
```

### Method 4: Create Standalone Executable (Windows Only)
```bash
# On your machine:
pip install pyinstaller
pyinstaller --onefile --windowed app.py

# Share the generated .exe file from dist/ folder
# Your friend just double-clicks to run (no installation needed)
```

---

## �🔍 Example Keywords

- "Machine Learning"
- "Sustainable Fashion"
- "Blockchain Gaming"
- "Remote Work Tools"
- "Cybersecurity Trends"

---

## ⚙️ Project Structure
```
Marketing engine/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

---

## � Deployment Options

### Option 1: Streamlit Cloud (Recommended - Free)
1. **Create a GitHub repository** with your project files
2. **Go to [share.streamlit.io](https://share.streamlit.io)**
3. **Connect your GitHub account**
4. **Select your repository and main file (`app.py`)**
5. **Deploy!** Get a public URL instantly

### Option 2: Local Installation (Share Project Folder)
1. **Zip the entire project folder**
2. **Send to your friend**
3. **They run:** `pip install -r requirements.txt && streamlit run app.py`

### Option 3: Railway (Free tier available)
1. **Connect GitHub repository**
2. **Railway auto-detects Python/Streamlit**
3. **Deploys automatically**

### Option 4: Heroku
1. **Create `Procfile`**: `web: streamlit run app.py --server.port $PORT`
2. **Deploy via GitHub integration**

---

## 📦 Sharing Instructions for Your Friend

| Package | Purpose | Free? |
|---------|---------|-------|
| `streamlit` | Web UI framework | Yes |
| `snscrape` | Reddit/Twitter scraping | Yes |
| `yt-dlp` | YouTube scraping | Yes |
| `beautifulsoup4` | HTML parsing | Yes |
| `requests` | HTTP requests | Yes |

---

## 🚨 Important Notes

### Rate Limiting
- **Reddit:** ~60 requests/minute (natural rate limiting)
- **Twitter/X:** May have IP-based limits
- **YouTube:** Generally responsive

**Solution:** If you hit limits, wait 15-30 minutes before retrying.

### Legal Considerations
✅ Public data scraping for research/marketing
✅ Complies with website terms where applicable
❌ Don't sell scraped data
❌ Don't violate platform ToS

### Common Issues

| Issue | Solution |
|-------|----------|
| "No posts found" | Try a more specific keyword |
| "Twitter timeout" | Wait 10-15 minutes, retry |
| "YouTube error" | Check internet connection |
| Slow scraping | Normal - wait 30-60 seconds |

---

## 🎯 Next Steps / Enhancements

- [ ] Add Sentiment Analysis (VADER, TextBlob)
- [ ] Implement keyword extraction (NLTK, spaCy)
- [ ] Create scheduling (APScheduler)
- [ ] Add database storage (SQLite)
- [ ] Export to CSV/JSON
- [ ] Free LLM integration (Ollama, Hugging Face)

---

## 📚 References & Resources

### Scraping Tools
- [snscrape Documentation](https://github.com/JustAnotherArchivist/snscrape)
- [yt-dlp GitHub](https://github.com/yt-dlp/yt-dlp)
- [Beautiful Soup Docs](https://www.crummy.com/software/BeautifulSoup/)

### Twitter/X Scraping After API Changes
- [snscrape Still Works](https://github.com/JustAnotherArchivist/snscrape/discussions)
- [yt-dlp for YouTube](https://github.com/yt-dlp/yt-dlp/wiki)

### Streamlit Docs
- [Streamlit Documentation](https://docs.streamlit.io)
- [Streamlit Caching](https://docs.streamlit.io/library/advanced-features/caching)

---

## 💡 Tips for Best Results

1.  **Be Specific:** "Python Web Development" > "Python"
2.  **Start Small:** Try one data source first, then add more
3.  **Test Keywords:** Iterate to find trending topics in your niche
4.  **Cache Results:** App caches data for 1 hour (faster re-runs)
5.  **Use as Inspiration:** Generated posts are starting points, add your flavor!

---

## 📄 License

This project is free to use for personal and commercial purposes.

---

## ❓ FAQ

**Q: Will this stop working?**
A: These tools are actively maintained. If one breaks, we can quickly switch to alternatives.

**Q: Can I use this for commercial purposes?**
A: Yes, but respect the platforms' ToS and terms of use for scraped data.

**Q: How do I increase post variety?**
A: Adjust the `analyze_keywords()` and `generate_social_posts()` functions to use better NLP.

**Q: Can I integrate paid APIs later?**
A: Yes! The code is modular—easily swap scraping functions with API calls.

---

Made with ❤️ for marketing teams that don't have API budgets.
