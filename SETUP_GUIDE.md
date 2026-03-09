# 🚀 Quick Setup Guide - Free Scraping Version

## What Changed? ✨

Your Marketing Engine is now **100% API-key free**. No more needing:
- Reddit credentials
- YouTube API keys  
- OpenAI/Gemini API keys
- HeyGen API keys

**Everything replaced with free, open-source tools.**

---

## Installation (5 Minutes)

### Windows Setup

```powershell
# Navigate to project directory
cd "C:\Users\aksha\OneDrive\Desktop\projects\Marketing engine"

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will automatically open at `http://localhost:8501`

**Easiest way: Double-click the batch file**
- Look for `run_app.bat` in your project folder
- Double-click it to start the app
- It will automatically activate the virtual environment and run Streamlit

---

## 🚀 Sharing with Friends

### Option 1: Deploy to Streamlit Cloud (Recommended)
1. Upload project to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect GitHub → Select repo → Deploy
4. Share the public URL!

### Option 2: Share Project Folder
- Zip the entire folder
- Send to friend
- They run: `pip install -r requirements.txt && streamlit run app.py`

### Option 3: Create Executable
- Run `create_exe.bat`
- Share the generated `.exe` file

**See `SHARE_WITH_FRIENDS.md` for detailed instructions!**

---

## Tools Installed

| Tool | What It Does | Why Free? |
|------|-------------|-----------|
| **snscrape** | Scrapes Reddit & Twitter posts | Open-source community project |
| **yt-dlp** | Downloads YouTube metadata | Maintained fork of youtube-dl |
| **Beautiful Soup** | Parses HTML | Popular open-source library |
| **Streamlit** | Web UI framework | Free tier available |

---

## Side-by-Side Comparison

### Old Approach (API Keys)
```
❌ Reddit API: Requires credentials
❌ YouTube API: $1-10/1000 requests
❌ OpenAI: $0.002-0.02 per request
❌ Gemini: Limited free tier
❌ HeyGen: $0.50+ per video
-------
Total Cost: $50-100+/month
```

### New Approach (Free Scraping)
```
✅ snscrape: Completely free
✅ yt-dlp: Completely free
✅ Template-based posts: Free
✅ Local processing: Free
✅ No subscriptions: Free
-------
Total Cost: $0/month ✨
```

---

## First Run

1. **Start the app:**
   ```bash
   streamlit run app.py
   ```

2. **Try a test search:**
   - Keyword: `Machine Learning trends`
   - Sources: Reddit + YouTube
   - Click "Generate Content"

3. **View results:**
   - Raw data collected
   - Generated social media posts
   - Copy/paste ready!

---

## Troubleshooting

### "ModuleNotFoundError: snscrape"
**Solution:** Ensure virtual environment is activated and requirements installed
```bash
venv\Scripts\activate
pip install -r requirements.txt
```

### "No posts found"
**Solution:** Try a more specific keyword
```
❌ "tech" → ✅ "AI tools 2024"
❌ "fitness" → ✅ "gym recovery techniques"
```

### "YouTube timeout"
**Solution:** This is normal for first run. Wait 30-60 seconds. Streamlit caches results, so second search is instant.

### "Twitter returns no results"
**Solution:** This is expected sometimes. Try different keywords or check X's current server status.

---

## Project Structure

```
Marketing engine/
├── app.py                 # Main application (refactored for free tools)
├── requirements.txt       # Dependencies (updated)
├── README.md             # Full documentation
├── SETUP_GUIDE.md        # This file
└── venv/                 # Virtual environment (created after setup)
```

---

## Advanced Usage

### Run in Background (Optional)
```bash
# On Windows, run permanently in background
streamlit run app.py --remote.runOnSave=false
```

### Use with Python Scheduler (Future Enhancement)
```python
# Could add later with APScheduler
# Schedule daily trending topic scrapes
```

### Export Results (Future Enhancement)
```python
# Could save to CSV/JSON
# import pandas as pd
# df.to_csv('trends.csv')
```

---

## Next Steps

1. ✅ **Install dependencies** (done below)
2. ✅ **Test with sample keyword** (Machine Learning)
3. ✅ **Try different data sources** (Reddit, X, YouTube)
4. 🔄 **Customize post templates** (in `generate_social_posts()` function)
5. 🔄 **Add AI model later** (Ollama, Hugging Face APIs)

---

## Key Advantages

| Feature | Benefit |
|---------|---------|
| **No API Keys** | Zero setup friction, instant start |
| **No Costs** | Save $50-100/month on APIs |
| **No Rate Limits** | Natural rate limiting built-in |
| **Open Source** | Full code visibility, community maintained |
| **Resilient** | Multiple fallback options available |
| **Local Processing** | Data stays on your machine |

---

## Command Reference

```bash
# Activate environment
venv\Scripts\activate

# Install new package (if needed)
pip install package_name

# Run app
streamlit run app.py

# Deactivate environment
deactivate

# Update requirements (after pip install)
pip freeze > requirements.txt
```

---

## Questions?

- **snscrape issues?** → GitHub: [JustAnotherArchivist/snscrape](https://github.com/JustAnotherArchivist/snscrape)
- **yt-dlp problems?** → GitHub: [yt-dlp/yt-dlp](https://github.com/yt-dlp/yt-dlp)
- **Streamlit help?** → Docs: [docs.streamlit.io](https://docs.streamlit.io)

---

Made with ❤️ for teams building marketing tools without API budgets!
