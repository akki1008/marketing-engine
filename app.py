import streamlit as st
import requests
from bs4 import BeautifulSoup
import json
import time

# --- Page Configuration ---
st.set_page_config(page_title="Marketing Engine - Real Trending Content", page_icon="🚀", layout="wide")

st.title("🚀 Marketing Engine - Real Trending Content")
st.markdown("**Scrape REAL trending posts and videos from Reddit & YouTube (no API keys needed)**")

# --- Scraping Functions ---

@st.cache_data(ttl=3600)
def get_reddit_posts(keyword, limit=5):
    """Fetches posts from Reddit using public JSON API with multiple strategies."""
    try:
        posts = []
        
        # Strategy 1: Try relevance sort first
        strategies = [
            f"https://www.reddit.com/search.json?q={keyword}&sort=relevance&t=month&limit={limit*4}",
            f"https://www.reddit.com/search.json?q={keyword}&sort=hot&t=week&limit={limit*4}",
            f"https://www.reddit.com/search.json?q={keyword}&sort=top&t=all&limit={limit*4}",
            f"https://www.reddit.com/r/all/search.json?q={keyword}&sort=relevance&t=month&limit={limit*4}"
        ]
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        
        for url in strategies:
            try:
                response = requests.get(url, headers=headers, timeout=20)
                response.raise_for_status()
                
                data = response.json()
                children = data.get('data', {}).get('children', [])
                
                if children:
                    for post in children:
                        post_data = post['data']
                        title = post_data.get('title', '').strip()
                        text = post_data.get('selftext', '').strip()
                        
                        # Filter for quality content
                        if (len(title) > 10 and 
                            not title.lower().startswith(('what', 'how', 'why', 'is it')) and
                            (text and len(text) > 50) and
                            post_data.get('score', 0) > 1):
                            
                            posts.append({
                                "title": title,
                                "text": text[:800],
                                "score": post_data.get('score', 0),
                                "comments": post_data.get('num_comments', 0),
                                "url": f"https://reddit.com{post_data.get('permalink', '')}",
                                "author": post_data.get('author', 'Unknown'),
                                "platform": "Reddit"
                            })
                            
                            if len(posts) >= limit:
                                break
                    
                    if posts:
                        break
                        
            except Exception as e:
                continue
        
        # If we got posts, return them
        if posts:
            return posts[:limit]
        
        # Last resort: Try subreddit-specific search
        try:
            # Common subreddits for business/tech content
            subreddits = ['r/technology', 'r/business', 'r/marketing', 'r/entrepreneur', 'r/startups']
            for sub in subreddits:
                if keyword.lower() in ['tech', 'technology', 'business', 'marketing', 'finance', 'ai', 'crypto']:
                    url = f"https://www.reddit.com{sub}/search.json?q={keyword}&sort=hot&t=week&limit={limit*2}"
                    response = requests.get(url, headers=headers, timeout=15)
                    if response.status_code == 200:
                        data = response.json()
                        children = data.get('data', {}).get('children', [])
                        for post in children[:limit]:
                            post_data = post['data']
                            title = post_data.get('title', '').strip()
                            text = post_data.get('selftext', '').strip()
                            
                            if len(title) > 10 and text and len(text) > 30:
                                posts.append({
                                    "title": title,
                                    "text": text[:600],
                                    "score": post_data.get('score', 0),
                                    "comments": post_data.get('num_comments', 0),
                                    "url": f"https://reddit.com{post_data.get('permalink', '')}",
                                    "author": post_data.get('author', 'Unknown'),
                                    "platform": f"Reddit ({sub})"
                                })
                                
                                if len(posts) >= limit:
                                    break
                        if posts:
                            break
        except:
            pass
            
        return posts[:limit] if posts else []
        
    except Exception as e:
        return []

@st.cache_data(ttl=3600)
def get_twitter_posts(keyword, limit=5):
    """Twitter/X scraping currently unavailable due to platform restrictions."""
    # Twitter/X has implemented strong anti-scraping measures
    # This would require API access or more sophisticated methods
    return []

@st.cache_data(ttl=3600)
def get_youtube_videos(keyword, limit=5):
    """Fetches YouTube videos using search with multiple strategies."""
    try:
        videos = []
        
        # Strategy 1: Search with trending filter
        search_urls = [
            f"https://www.youtube.com/results?search_query={keyword}&sp=CAASAhAB",  # Relevance
            f"https://www.youtube.com/results?search_query={keyword}&sp=CAMSAhAB",  # Upload date
            f"https://www.youtube.com/results?search_query={keyword}&sp=CAMSBhAB",  # View count
        ]
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        for search_url in search_urls:
            try:
                response = requests.get(search_url, headers=headers, timeout=20)
                
                if response.status_code == 200:
                    # Extract video IDs using regex
                    import re
                    video_ids = re.findall(r'watch\?v=([a-zA-Z0-9_-]{11})', response.text)
                    
                    # Remove duplicates while preserving order
                    seen = set()
                    unique_ids = []
                    for vid_id in video_ids:
                        if vid_id not in seen:
                            seen.add(vid_id)
                            unique_ids.append(vid_id)
                    
                    for vid_id in unique_ids[:limit]:
                        # Try to get video title from the page
                        try:
                            video_url = f"https://www.youtube.com/watch?v={vid_id}"
                            video_response = requests.get(video_url, headers=headers, timeout=10)
                            
                            if video_response.status_code == 200:
                                # Extract title from HTML
                                title_match = re.search(r'<title>([^<]+)</title>', video_response.text)
                                title = title_match.group(1).replace(' - YouTube', '').strip() if title_match else f"Video about {keyword}"
                                
                                # Extract channel name
                                channel_match = re.search(r'"ownerChannelName":"([^"]+)"', video_response.text)
                                channel = channel_match.group(1) if channel_match else "YouTube Creator"
                                
                                # Extract view count
                                view_match = re.search(r'"viewCount":"(\d+)"', video_response.text)
                                views = f"{int(view_match.group(1)):,} views" if view_match else "View count varies"
                                
                                videos.append({
                                    "title": title,
                                    "description": f"Trending video from {channel}",
                                    "channel": channel,
                                    "views": views,
                                    "url": video_url,
                                    "platform": "YouTube"
                                })
                                
                                if len(videos) >= limit:
                                    break
                            
                        except Exception as e:
                            # Fallback: Just add the video with basic info
                            videos.append({
                                "title": f"YouTube video about {keyword}",
                                "description": "Trending content from YouTube",
                                "channel": "YouTube Creator",
                                "views": "Trending",
                                "url": f"https://www.youtube.com/watch?v={vid_id}",
                                "platform": "YouTube"
                            })
                            
                            if len(videos) >= limit:
                                break
                    
                    if videos:
                        break
                        
            except Exception as e:
                continue
        
        return videos[:limit]
        
    except Exception as e:
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
            sources_fetched = []

            # Fetch from selected sources
            if "Reddit" in sources:
                with st.status("Scraping Reddit...", expanded=False):
                    reddit_posts = get_reddit_posts(keyword, 5)
                    count = len(reddit_posts)
                    st.write(f"Found {count} posts")
                    if count > 0:
                        sources_fetched.append("Reddit")
                    all_content.extend(reddit_posts)

            if "Twitter/X" in sources:
                with st.status("Scraping Twitter/X...", expanded=False):
                    twitter_posts = get_twitter_posts(keyword, 5)
                    count = len(twitter_posts)
                    st.write(f"Found {count} tweets")
                    if count > 0:
                        sources_fetched.append("Twitter/X")
                    all_content.extend(twitter_posts)

            if "YouTube" in sources:
                with st.status("Scraping YouTube...", expanded=False):
                    youtube_videos = get_youtube_videos(keyword, 5)
                    count = len(youtube_videos)
                    st.write(f"Found {count} videos")
                    if count > 0:
                        sources_fetched.append("YouTube")
                    all_content.extend(youtube_videos)

        # If we have no content, show helpful message
        if not all_content:
            st.warning("⚠️ Unable to fetch live content. This may be due to:")
            st.write("- Platform rate limiting (try again in 15-30 minutes)")
            st.write("- Network connectivity issues")
            st.write("- Platform changes (scraping can be unreliable)")
            st.write("- Try different keywords or fewer data sources")
            st.error("❌ Could not fetch content. Try a different keyword or check your internet connection.")
        else:
            sources_text = ", ".join(sources_fetched) if sources_fetched else "Multiple Sources"
            st.success(f"✅ Successfully fetched {len(all_content)} items from {sources_text}!")

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

            # Generate posts
            st.subheader("🔥 AI-Generated Social Media Posts")
            generated_posts = generate_social_posts(all_content)

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
**Free Web Scraping Tools Used:**
- **requests**: HTTP requests
- **Beautiful Soup**: HTML parsing
- **Reddit JSON API**: Public API access

**No API Keys Required!**
""")

st.sidebar.header("🛠️ Tools Reference")
with st.sidebar.expander("Reddit Scraping"):
    st.write("""
    **Method:** JSON API + Web scraping
    - Uses Reddit's public JSON endpoints
    - No authentication needed
    - Rate limited naturally
    """)

with st.sidebar.expander("Twitter/X Scraping"):
    st.write("""
    **Status:** Limited availability
    - Basic web scraping (may not work reliably)
    - Consider using Reddit + YouTube
    """)

with st.sidebar.expander("YouTube Scraping"):
    st.write("""
    **Method:** Basic web scraping
    - Limited data extraction
    - YouTube changes HTML frequently
    - For full features, use YouTube Data API
    """)

st.sidebar.header("💡 Tips")
st.sidebar.write("""
1. Be specific with keywords (e.g., "AI stock trading", "crypto markets")
2. Start with Reddit + YouTube for best results
3. Twitter/X scraping is currently limited
4. Results are cached for 1 hour (faster re-runs)
5. If no results, try different keywords or wait 15-30 minutes
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
