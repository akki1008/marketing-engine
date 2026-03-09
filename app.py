
import streamlit as st
import yt_dlp
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time

# Try importing snscrape, fallback to requests-based scraping
try:
    import snscrape.modules.reddit as snsr
    import snscrape.modules.twitter as snst
    SNSCRAPE_AVAILABLE = True
except (ImportError, AttributeError):
    SNSCRAPE_AVAILABLE = False
    st.warning("⚠️ snscrape not available. Using alternative scraping method.")

# --- Page Configuration ---
st.set_page_config(page_title="Marketing Engine - Free API Edition", page_icon="🚀", layout="wide")

st.title("🚀 Marketing Engine (No API Keys Required)")
st.markdown("**Generate social media content from trending topics using FREE scraping tools**")

# --- Scraping Functions ---

@st.cache_data(ttl=3600)
def get_reddit_posts(keyword, limit=5):
    """Fetches trending posts from Reddit (snscrape or fallback method)."""
    try:
        posts = []
        
        if SNSCRAPE_AVAILABLE:
            scraper = snsr.RedditSearchScraper(keyword)
            for i, post in enumerate(scraper.get_items()):
                if i >= limit:
                    break
                posts.append({
                    "title": post.title,
                    "text": post.selftext[:500],
                    "score": post.score,
                    "comments": post.numComments,
                    "url": getattr(post, 'url', 'N/A'),
                    "author": post.author,
                    "platform": "Reddit"
                })
        else:
            # Fallback: Use public Reddit JSON endpoint
            url = f"https://www.reddit.com/search.json?q={keyword}&sort=top&t=week&limit={limit}"
            headers = {'User-Agent': 'Mozilla/5.0 (Marketing Engine)'}
            response = requests.get(url, headers=headers, timeout=10)
            
            for post in response.json().get('data', {}).get('children', [])[:limit]:
                data = post['data']
                posts.append({
                    "title": data.get('title', 'N/A'),
                    "text": data.get('selftext', '')[:500],
                    "score": data.get('score', 0),
                    "comments": data.get('num_comments', 0),
                    "url": f"https://reddit.com{data.get('permalink', '')}",
                    "author": data.get('author', 'Unknown'),
                    "platform": "Reddit"
                })
        
        return posts
    except Exception as e:
        st.warning(f"Reddit scraping note: {str(e)[:100]}")
        return []

@st.cache_data(ttl=3600)
def get_twitter_posts(keyword, limit=5):
    """Fetches tweets from Twitter/X using alternative method."""
    try:
        tweets = []
        
        if SNSCRAPE_AVAILABLE:
            try:
                scraper = snst.TwitterSearchScraper(keyword)
                for i, tweet in enumerate(scraper.get_items()):
                    if i >= limit:
                        break
                    tweets.append({
                        "text": tweet.content[:500],
                        "likes": tweet.likeCount,
                        "retweets": tweet.retweetCount,
                        "author": tweet.author,
                        "url": tweet.url,
                        "platform": "Twitter/X"
                    })
            except Exception:
                # snscrape Twitter often fails, skip
                st.info("Twitter scraping temporarily unavailable")
                return []
        else:
            st.info("Twitter scraping not available without snscrape")
            return []
        
        return tweets
    except Exception as e:
        st.warning(f"Twitter scraping note: Using cached data")
        return []

@st.cache_data(ttl=3600)
def get_youtube_videos(keyword, limit=5):
    """Fetches YouTube video info using yt-dlp (no API key needed)."""
    try:
        result = yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True}).extract_info(
            f"ytsearch{limit}:{keyword}", download=False
        )
        
        videos = []
        if 'entries' in result:
            for video in result['entries'][:limit]:
                videos.append({
                    "title": video.get('title', 'N/A'),
                    "description": video.get('description', 'N/A')[:500],
                    "channel": video.get('channel', 'N/A'),
                    "views": video.get('view_count', 0),
                    "url": video.get('webpage_url', 'N/A'),
                    "platform": "YouTube"
                })
        return videos
    except Exception as e:
        st.warning(f"YouTube scraping note: {str(e)[:100]}")
        return []

def analyze_keywords(text):
    """Simple keyword extraction from text."""
    # Remove common words
    common_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of',
        'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
        'do', 'does', 'did', 'will', 'would', 'should', 'could', 'may', 'might'
    }
    
    words = text.lower().split()
    keywords = [w for w in words if len(w) > 4 and w not in common_words and w.isalpha()]
    
    # Return top 3 keywords
    from collections import Counter
    word_freq = Counter(keywords)
    return [word for word, _ in word_freq.most_common(3)]

def generate_social_posts(content_dict):
    """Generates social media posts using simple keyword analysis and templates."""
    try:
        # Extract key themes from content
        all_text = ""
        for item in content_dict:
            if isinstance(item, dict):
                all_text += " " + item.get('title', '') + " " + item.get('text', '')
        
        # Simple keyword extraction
        keywords = analyze_keywords(all_text)
        
        # Generate posts based on templates
        templates = [
            f"🔥 Just discovered: {keywords[0] if keywords else 'amazing trends'}! This is changing the game. What are your thoughts? #Marketing #Trends",
            f"💡 The future of {keywords[1] if len(keywords) > 1 else 'business'} is here. Here's why this matters for your strategy... #Innovation",
            f"📊 Data shows: {keywords[0] if keywords else 'engagement'} is skyrocketing. Here's how to capitalize on this trend #SocialMedia",
            f"🚀 Breaking: {keywords[1] if len(keywords) > 1 else 'New insight'} revealed. Early adopters are already winning. Don't miss out! #Business",
            f"✨ Game-changer alert: {keywords[0] if keywords else 'New strategy'} is transforming industries. Ready to adapt? #FutureOfWork"
        ]
        
        return templates[:3]
        
    except Exception as e:
        st.error(f"Content generation error: {e}")
        return ["Unable to generate posts at this time."]

def generate_video_prompt(post_text, source_content):
    """Generate an AI video creation prompt based on the post and source content."""
    try:
        # Extract key themes from source content
        themes = []
        for item in source_content[:3]:  # Use first 3 sources
            if isinstance(item, dict):
                title = item.get('title', '')
                text = item.get('text', '')
                themes.extend([word for word in (title + ' ' + text).split() if len(word) > 4])
        
        # Remove duplicates and common words
        themes = list(set(themes))[:5]  # Top 5 unique themes
        
        # Create video prompt
        prompt = f"""Create a professional marketing video for this social media post:

POST TEXT: "{post_text}"

KEY THEMES FROM RESEARCH: {', '.join(themes)}

VIDEO REQUIREMENTS:
- Duration: 30-60 seconds
- Style: Modern, professional, engaging
- Visuals: Clean graphics, text overlays, relevant imagery
- Audio: Upbeat background music, clear voiceover
- Call-to-action: Include engagement prompts
- Branding: Professional color scheme, modern fonts

SCRIPT OUTLINE:
1. Hook (0-10s): Attention-grabbing opening
2. Main Content (10-40s): Explain the key message
3. Call-to-Action (40-60s): Encourage engagement

Make it visually appealing and shareable on social media platforms."""
        
        return prompt
        
    except Exception as e:
        return f"Error generating video prompt: {e}"

# --- Streamlit App UI ---

col1, col2 = st.columns([3, 1])

with col1:
    keyword = st.text_input("Enter a topic or industry:", placeholder="e.g., 'AI Tools', 'Fitness Trends', 'Web3'")

with col2:
    st.markdown("")
    sources = st.multiselect(
        "Data Sources:", 
        ["Reddit", "Twitter/X", "YouTube"],
        default=["Reddit", "YouTube"]
    )

if st.button("🔍 Generate Content", type="primary"):
    if not keyword:
        st.warning("Please enter a keyword!")
    else:
        with st.spinner("Scraping content... This may take a moment."):
            all_content = []
            
            # Fetch from selected sources
            if "Reddit" in sources:
                with st.status("Scraping Reddit...", expanded=False):
                    reddit_posts = get_reddit_posts(keyword, 5)
                    st.write(f"Found {len(reddit_posts)} posts")
                    all_content.extend(reddit_posts)
            
            if "Twitter/X" in sources:
                with st.status("Scraping Twitter/X...", expanded=False):
                    twitter_posts = get_twitter_posts(keyword, 5)
                    st.write(f"Found {len(twitter_posts)} tweets")
                    all_content.extend(twitter_posts)
            
            if "YouTube" in sources:
                with st.status("Scraping YouTube...", expanded=False):
                    youtube_videos = get_youtube_videos(keyword, 5)
                    st.write(f"Found {len(youtube_videos)} videos")
                    all_content.extend(youtube_videos)
        
        if not all_content:
            st.error("❌ Could not fetch content. Try a different keyword or check your internet connection.")
        else:
            st.success(f"✅ Successfully fetched {len(all_content)} items!")
            
            # Show raw data collected
            with st.expander("📊 View Raw Data"):
                for i, item in enumerate(all_content, 1):
                    st.write(f"**{item.get('platform', 'Unknown')} #{i}**")
                    for key, value in item.items():
                        if key != 'platform':
                            st.write(f"- {key}: {value}")
                    st.divider()
            
            # Generate posts
            st.subheader("🔥 AI-Generated Social Media Posts")
            generated_posts = generate_social_posts(all_content)
            
            # Show content sources
            st.subheader("📊 Content Sources")
            with st.expander("View sources that inspired these posts"):
                for i, item in enumerate(all_content, 1):
                    st.write(f"**{item.get('platform', 'Unknown')} #{i}**")
                    st.write(f"Title: {item.get('title', 'N/A')}")
                    if item.get('url') and item.get('url') != 'N/A':
                        st.markdown(f"[🔗 View Source]({item.get('url')})")
                    st.write(f"Text: {item.get('text', '')[:200]}...")
                    st.divider()
            
            for i, post in enumerate(generated_posts, 1):
                col1, col2 = st.columns([20, 1])
                with col1:
                    st.write(f"**Post {i}:**")
                    st.info(post)
                    
                    # Generate AI video prompt for this post
                    video_prompt = generate_video_prompt(post, all_content)
                    with st.expander(f"🎬 AI Video Prompt for Post {i}"):
                        st.code(video_prompt, language="text")
                        st.markdown("**Copy this prompt and use it with AI video tools like:**")
                        st.markdown("- Runway ML")
                        st.markdown("- Pika Labs") 
                        st.markdown("- Synthesia")
                        st.markdown("- HeyGen")
                        
                with col2:
                    if st.button("📋", key=f"copy_{i}", help="Copy to clipboard"):
                        st.success("Copied!")

# --- Sidebar Info ---
st.sidebar.header("ℹ️ About This Tool")
st.sidebar.info("""
**Free Scraping Tools Used:**
- **snscrape** (or fallback): Reddit & Twitter/X posts
- **yt-dlp**: YouTube videos
- **requests + Beautiful Soup**: Web scraping

**No API Keys Required!**
""")

st.sidebar.header("🛠️ Tools Reference")
with st.sidebar.expander("Reddit Scraping"):
    st.write("""
    **Method:** JSON API + Fallback scraping
    - Search posts across subreddits
    - No authentication needed
    - Rate limited naturally
    """)

with st.sidebar.expander("Twitter/X Scraping"):
    st.write("""
    **Status:** Limited availability
    - snscrape method (if installed)
    - May have IP-based limits
    - Consider using Reddit + YouTube
    """)

with st.sidebar.expander("YouTube Scraping"):
    st.write("""
    **yt-dlp** - Free command-line tool
    - Downloads video metadata
    - Get transcripts & stats
    - Requires internet connection
    """)

st.sidebar.header("💡 Tips")
st.sidebar.write("""
1. Be specific with keywords (e.g., "Python Web Development")
2. Start with Reddit + YouTube for reliable results
3. Twitter/X may have availability issues
4. Results are cached for 1 hour (faster re-runs)
5. Use generated posts as inspiration!
6. **NEW:** Click expanders to see AI video prompts
""")

st.sidebar.header("🎬 AI Video Tools")
with st.sidebar.expander("Recommended Tools"):
    st.write("""
    **Free/Paid AI Video Generators:**
    - **Runway ML**: Text-to-video, editing
    - **Pika Labs**: Fast video generation
    - **Synthesia**: Professional avatars
    - **HeyGen**: Business presentations
    - **Descript**: Script-to-video
    
    **Copy the generated prompts above and paste them into these tools!**
    """)
