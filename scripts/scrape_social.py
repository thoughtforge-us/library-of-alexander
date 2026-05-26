#!/usr/bin/env python3
"""Library of Alexander — Social Discovery Engine v2

Scrapes 8 sources + 100+ RSS feeds for AI tool/research discoveries.
Zero new deps — stdlib + requests + yt-dlp (all on Luna).
Saves JSON + markdown summary. Rotates feeds to spread load.

Run:  python3 scripts/scrape_social.py [--sources all] [--max-feeds 20]
Cron: */30 * * * * python3 /path/to/scrape_social.py --output-dir /tmp/library-of-alexander/data/discoveries
"""

import os, sys, re, json, time, subprocess, html, urllib.parse, random
from pathlib import Path
from datetime import datetime, timezone
from xml.etree import ElementTree

try: import requests
except: requests = None

LIBRARY_DIR = Path(__file__).parent.parent
OUTPUT_DIR = LIBRARY_DIR / "data" / "discoveries"
TIMEOUT = 15
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
CURSOR_FILE = LIBRARY_DIR / "data" / "rss_cursor.txt"
MAX_FEEDS_PER_RUN = 20

os.makedirs(OUTPUT_DIR, exist_ok=True)
if CURSOR_FILE.parent: os.makedirs(CURSOR_FILE.parent, exist_ok=True)

def log(msg): print(f"[{datetime.now():%H:%M:%S}] {msg}")

def safe_get(url, headers=None, params=None, timeout=TIMEOUT):
    if not requests: return None
    try:
        h = {"User-Agent": UA, "Accept": "application/json,text/html,*/*"}
        if headers: h.update(headers)
        r = requests.get(url, headers=h, params=params, timeout=timeout)
        if r.status_code == 200: return r
    except: pass
    return None

def extract_links(text):
    links = []
    for pat in [
        r'github\.com/([\w-]+/[\w.-]+)',
        r'arxiv\.org/abs/(\d+\.\d+)',
        r'huggingface\.co/([\w-]+/[\w.-]+)',
    ]:
        links.extend(re.findall(pat, text, re.I))
    return list(set(links))


# ═══════════════════════════════════════════════════════════════
# RSS FEED ENGINE (100+ AI feeds from companies, research, news)
# ═══════════════════════════════════════════════════════════════

RSS_FEEDS = {
    # ── AI News & Journalism ──
    "ai-news-techcrunch": "https://techcrunch.com/category/artificial-intelligence/feed",
    "ai-news-venturebeat": "https://venturebeat.com/category/ai/feed",
    "ai-news-arstechnica": "https://arstechnica.com/ai/feed",
    "ai-news-theverge": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
    "ai-news-wired": "https://www.wired.com/feed/tag/ai/latest/rss",
    "ai-news-mit": "http://news.mit.edu/rss/topic/artificial-intelligence2",
    "ai-news-nytimes": "https://www.nytimes.com/svc/collections/v1/publish/https://www.nytimes.com/spotlight/artificial-intelligence/rss.xml",
    "ai-news-guardian": "https://www.theguardian.com/technology/artificialintelligenceai/rss",
    "ai-news-techreview": "https://www.technologyreview.com/topic/artificial-intelligence/feed",
    "ai-news-fastcompany": "https://www.fastcompany.com/section/artificial-intelligence/rss",
    "ai-news-ft": "https://www.ft.com/artificial-intelligence?format=rss",
    "ai-news-unite": "https://www.unite.ai/feed",
    "ai-news-aitrends": "https://www.aitrends.com/feed",
    "ai-news-dailyai": "https://dailyai.com/feed",
    "ai-news-insideainews": "https://insideainews.com/feed",
    "ai-news-aiwire": "https://www.aiwire.net/feed",
    "ai-news-theaiinsider": "https://theaiinsider.tech/feed",
    "ai-news-artificialintelnews": "https://www.artificialintelligence-news.com/feed",
    "ai-news-aiforgood": "https://aiforgood.itu.int/feed",
    "ai-news-aihub": "https://aihub.org/feed",
    "ai-news-aiworldjournal": "https://aiworldjournal.com/feed",

    # ── AI Research & Academic ──
    "ai-research-google": "http://ai.googleblog.com/feeds/posts/default",
    "ai-research-bair": "https://bair.berkeley.edu/blog/feed.xml",
    "ai-research-deepmind": "https://research.google/blog/rss/",
    "ai-research-openai": "https://openai.com/news/rss.xml",
    "ai-research-intelligence": "https://intelligence.org/feed",
    "ai-research-kdnuggets": "http://www.kdnuggets.com/feed",
    "ai-research-mastery": "https://machinelearningmastery.com/blog/feed",
    "ai-research-oreilly": "https://www.oreilly.com/radar/topics/ai-ml/feed/index.xml",
    "ai-research-rstudio": "https://blogs.rstudio.com/ai/index.xml",
    "ai-research-aisummer": "https://theaisummer.com/feed.xml",
    "ai-research-qudata": "https://qudata.com/en/news/rss.xml",

    # ── arXiv Categories ──
    "arxiv-cs-ai": "http://export.arxiv.org/rss/cs.AI",
    "arxiv-cs-lg": "http://export.arxiv.org/rss/cs.LG",
    "arxiv-cs-cl": "http://export.arxiv.org/rss/cs.CL",
    "arxiv-cs-cv": "http://export.arxiv.org/rss/cs.CV",
    "arxiv-cs-ro": "http://export.arxiv.org/rss/cs.RO",
    "arxiv-cs-se": "http://export.arxiv.org/rss/cs.SE",
    "arxiv-stat-ml": "http://export.arxiv.org/rss/stat.ML",
    "arxiv-paperswithcode": "https://paperswithcode.com/rss",

    # ── AI Company Blogs ──
    "company-openai": "https://openai.com/news/rss.xml",
    "company-ibm": "https://www.ibm.com/think/feed",
    "company-aws-ml": "https://aws.amazon.com/blogs/machine-learning/category/artificial-intelligence/feed",
    "company-microsoft": "https://news.microsoft.com/source/topics/ai/feed",
    "company-cisco": "https://blogs.cisco.com/ai/feed",
    "company-sas": "https://blogs.sas.com/content/topic/artificial-intelligence/feed",
    "company-nvidia-blog": "https://developer.nvidia.com/blog/feed",
    "company-nvidia": "https://blogs.nvidia.com/feed/",
    "company-huggingface": "https://huggingface.co/blog/feed.xml",
    "company-databricks": "https://www.databricks.com/feed",
    "company-anyscale": "https://www.anyscale.com/blog/feed",
    "company-datarobot": "https://www.datarobot.com/blog/feed",
    "company-nanonets": "https://nanonets.com/blog/rss",
    "company-clarifai": "https://www.clarifai.com/blog/rss.xml",
    "company-alephalpha": "https://aleph-alpha.com/feed",
    "company-contextual": "https://contextual.ai/blog/feed",
    "company-copyleaks": "https://copyleaks.com/blog/feed",
    "company-gptzero": "https://gptzero.me/news/rss",
    "company-elevenlabs": "https://elevenlabs.io/feed.xml",

    # ── AI Newsletters & Substacks ──
    "nl-semianalysis": "https://semianalysis.com/feed/",
    "nl-oneusefulthing": "https://www.oneusefulthing.org/feed",
    "nl-lastweekin": "https://lastweekin.ai/feed",
    "nl-importai": "https://importai.net/feed",
    "nl-latentspace": "https://latent.space/feed",
    "nl-cameronwolfe": "https://cameronrwolfe.substack.com/feed",
    "nl-ethanzuckerman": "https://ethanzuckerman.substack.com/feed",
    "nl-aisupremacy": "https://aisupremacy.substack.com/feed",
    "nl-algorithmicbridge": "https://thealgorithmicbridge.substack.com/feed",
    "nl-ruder-io": "https://newsletter.ruder.io/feed",
    "nl-datamachina": "https://datamachina.substack.com/feed",
    "nl-zerothprinciples": "https://zerothprinciples.substack.com/feed",

    # ── Personal AI Blogs ──
    "blog-simonwillison": "https://simonwillison.net/atom/everything/",
    "blog-lilianweng": "https://lilianweng.github.io/feed.xml",
    "blog-jaykmody": "https://jaykmody.com/feed.xml",
    "blog-sebastianraschka": "https://www.sebastianraschka.com/blog/feed",
    "blog-everyone": "https://ai.googleblog.com/feeds/posts/default",

    # ── AI Industry & Platforms ──
    "platform-wandb": "https://www.wandb.ai/articles/feed",
    "platform-comet": "https://www.comet.com/blog/feed",
    "platform-mlflow": "https://www.mlflow.org/blog/rss.xml",
    "platform-flyte": "https://www.flyte.org/blog/feed",
    "platform-gradient": "https://www.gradient.ai/feed",
    "platform-kore": "https://blog.kore.ai/rss.xml",
    "platform-vue": "https://www.vue.ai/blog/feed",

    # ── AI Tool Discovery ──
    "tools-becominghuman": "https://becominghuman.ai/feed",
    "tools-ai2people": "https://ai2people.com/feed",
    "tools-aicorr": "https://aicorr.com/feed",
    "tools-airevolution": "https://airevolution.blog/feed",
    "tools-deepcognition": "https://deepcognition.ai/feed",
    "tools-dlabs": "https://dlabs.ai/feed",
    "tools-saal": "https://saal.ai/feed",
    "tools-shaip": "https://www.shaip.com/feed",
    "tools-fusemachines": "https://insights.fusemachines.com/feed",
    "tools-topmarketingai": "https://topmarketingai.com/feed",
    "tools-marketingai": "http://www.marketingaiinstitute.com/blog/rss.xml",
    "tools-artisse": "https://artisse.ai/feed",
    "tools-sdexample": "https://www.sdexample.com/feeds/posts/default",
    "tools-aitensorflow": "https://www.aitrends.com/feed",

    # ── AI in Government & Law ──
    "gov-govtech": "https://www.govtech.com/artificial-intelligence.rss",
    "gov-federalnews": "https://federalnewsnetwork.com/category/technology-main/artificial-intelligence/feed",
    "law-artificial-lawyer": "https://www.artificiallawyer.com/feed",
    "law-aitlaw": "https://www.aitechnologylaw.com/feed",
    "news-crunchbase": "https://news.crunchbase.com/sections/ai/feed",
    "news-geekwire": "https://www.geekwire.com/tag/ai/feed",
    "news-adweek": "https://www.adweek.com/category/artificial-intelligence/feed",
    "news-indianexpress": "https://indianexpress.com/section/technology/artificial-intelligence/feed",

    # ── AI Conference & Media ──
    "media-danrose": "https://www.danrose.ai/blog",
    "media-berkshire": "https://www.berkshiregrey.com/feed",
    "media-quertle": "https://quertle.com/feed",
    "media-dxcover": "https://www.dxcover.com/feed",
    "media-neysa": "https://neysa.ai/feed",
    "media-cogito": "https://www.cogitotech.com/feed",
    "media-suno": "https://www.suno.ai/blog/feed",

    # ── Chinese AI Ecosystem ──
    "chinese-zhihu": "https://zhuanlan.zhihu.com/feed",
}

RSS_FEED_LIST = list(RSS_FEEDS.items())

def get_rss_batch():
    """Get next batch of feeds to scrape using cursor rotation."""
    cursor = 0
    if CURSOR_FILE.exists():
        try: cursor = int(CURSOR_FILE.read_text().strip())
        except: cursor = 0

    batch = RSS_FEED_LIST[cursor:cursor + MAX_FEEDS_PER_RUN]
    if len(batch) < MAX_FEEDS_PER_RUN:
        remaining = RSS_FEED_LIST[:MAX_FEEDS_PER_RUN - len(batch)]
        batch.extend(remaining)

    new_cursor = (cursor + MAX_FEEDS_PER_RUN) % len(RSS_FEED_LIST)
    CURSOR_FILE.write_text(str(new_cursor))

    log(f"RSS: processing {len(batch)} feeds (cursor: {cursor}→{new_cursor}/{len(RSS_FEED_LIST)})")
    return batch

def parse_feed(name, url):
    """Parse an RSS/Atom feed and return items."""
    if not requests: return []
    try:
        r = safe_get(url, timeout=20)
        if not r: return []
        text = r.text
        items = []

        def _match(pat, src, grp=1, strip_tags=True):
            m = re.search(pat, src, re.DOTALL)
            if not m: return ""
            val = m.group(grp)
            if strip_tags: val = re.sub(r'<[^>]+>', '', val)
            return html.unescape(val).strip()

        def _link(entry):
            m = re.search(r'<link>(.*?)</link>', entry, re.DOTALL)
            if m: return m.group(1).strip()
            m = re.search(r'<link[^>]*href="([^"]+)"', entry)
            if m: return m.group(1).strip()
            return ""

        # Try RSS
        for item in re.findall(r'<item>(.*?)</item>', text, re.DOTALL):
            title = _match(r'<title>(.*?)</title>', item)
            if not title: continue
            link = _link(item)
            desc = _match(r'<description>(.*?)</description>', item)[:500]
            pubdate = _match(r'<pubDate>(.*?)</pubDate>', item, strip_tags=False)
            items.append({"title": title, "url": link, "description": desc, "published": pubdate})

        # Try Atom
        if not items:
            for entry in re.findall(r'<entry>(.*?)</entry>', text, re.DOTALL):
                title = _match(r'<title>(.*?)</title>', entry)
                if not title: continue
                link = _link(entry)
                desc = _match(r'<content[^>]*>(.*?)</content>', entry)[:500]
                updated = _match(r'<updated>(.*?)</updated>', entry, strip_tags=False)
                items.append({"title": title, "url": link, "description": desc, "published": updated})

        return items[:10]
    except Exception as e:
        log(f"  RSS error {name}: {e}")
        return []

def scrape_rss():
    """Scrape RSS feeds, rotating batch each run."""
    if not requests: return []
    batch = get_rss_batch()
    found = []

    for name, url in batch:
        if not url: continue
        category = name.split("-")[0] if "-" in name else "other"
        items = parse_feed(name, url)
        for item in items:
            links = extract_links(item["title"] + " " + item["description"])
            found.append({
                "source": "rss",
                "feed": name,
                "category": category,
                "title": item["title"],
                "description": item["description"],
                "url": item["url"],
                "published": item["published"],
                "links": links,
            })
        log(f"  RSS {name}: {len(items)} items")
        time.sleep(0.5)

    return found


# ═══════════════════════════════════════════════════════════════
# REDDIT
# ═══════════════════════════════════════════════════════════════

REDDIT_SUBREDDITS = [
    "MachineLearning", "LocalLLaMA", "artificialintelligence",
    "opensource", "selfhosted", "StableDiffusion",
    "comfyui", "LLMDevs", "LangChain",
]

def scrape_reddit(subreddits=None, limit=10):
    if not requests: return []
    subreddits = subreddits or REDDIT_SUBREDDITS
    found = []
    for sub in subreddits:
        try:
            r = safe_get(f"https://www.reddit.com/r/{sub}/hot.json?limit={limit}")
            if not r: continue
            data = r.json()
            for child in data.get("data", {}).get("children", []):
                d = child.get("data", {})
                title = d.get("title", "")
                selftext = (d.get("selftext") or "")[:500]
                url = d.get("url", "")
                score = d.get("score", 0)
                comments = d.get("num_comments", 0)
                permalink = f"https://www.reddit.com{d.get('permalink','')}"
                links = extract_links(title + " " + selftext)
                found.append({
                    "source": "reddit", "subreddit": sub,
                    "title": html.unescape(title),
                    "score": score, "comments": comments,
                    "url": url, "permalink": permalink,
                    "links": links,
                })
            log(f"  Reddit /r/{sub}: posts")
            time.sleep(1)
        except Exception as e:
            log(f"  Reddit /r/{sub} error: {e}")
    return found


# ═══════════════════════════════════════════════════════════════
# YOUTUBE via yt-dlp
# ═══════════════════════════════════════════════════════════════

YOUTUBE_QUERIES = [
    "AI tools open source 2026", "best AI tools", "local LLM setup",
    "AI agent framework tutorial", "open source LLM comparison",
    "RAG tutorial", "ComfyUI workflow", "AI coding assistant",
    "self hosted AI", "machine learning tools",
]

def search_youtube(query, max_results=5):
    entries = []
    try:
        q = query.replace('"', '\\"')
        cmd = f'yt-dlp --flat-playlist -s -J "ytsearch{max_results}:{q}" 2>/dev/null'
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        if r.returncode != 0: return entries
        data = json.loads(r.stdout)
        for e in data.get("entries", []):
            vid = e.get("id", "")
            entries.append({
                "source": "youtube", "query": query,
                "title": e.get("title", ""), "channel": e.get("channel", ""),
                "url": f"https://youtube.com/watch?v={vid}",
                "views": e.get("view_count", 0), "duration": e.get("duration", 0),
            })
    except: pass
    return entries

def scrape_youtube():
    found = []
    for q in YOUTUBE_QUERIES:
        results = search_youtube(q)
        found.extend(results)
        log(f"  YouTube '{q[:40]}': {len(results)} videos")
        time.sleep(2)
    return found


# ═══════════════════════════════════════════════════════════════
# TIKTOK via tikwm.com API
# ═══════════════════════════════════════════════════════════════

TIKTOK_QUERIES = [
    "AI tools", "artificial intelligence", "machine learning",
    "open source AI", "AI coding", "AI agent",
]

def scrape_tiktok(queries=None, count=10):
    if not requests: return []
    queries = queries or TIKTOK_QUERIES
    found = []
    for q in queries:
        try:
            r = safe_get("https://www.tikwm.com/api/feed/search",
                         params={"keywords": q, "count": count})
            if not r: continue
            data = r.json()
            for item in data.get("data", {}).get("videos", []):
                desc = item.get("title", item.get("desc", ""))
                found.append({
                    "source": "tiktok", "query": q,
                    "description": html.unescape(desc)[:200],
                    "author": item.get("author", item.get("unique_id", "unknown")),
                    "url": f"https://www.tiktok.com/@{item.get('unique_id','')}/video/{item.get('video_id','')}",
                    "plays": item.get("play_count", 0), "likes": item.get("digg_count", 0),
                    "links": extract_links(desc),
                })
            log(f"  TikTok '{q}': {len(data.get('data',{}).get('videos',[]))} videos")
            time.sleep(1)
        except: pass
    return found


# ═══════════════════════════════════════════════════════════════
# TWITTER/X via Nitter
# ═══════════════════════════════════════════════════════════════

TWITTER_QUERIES = [
    "AI tools", "open source AI", "machine learning",
    "LLM", "AI agent", "artificial intelligence",
]

def parse_nitter_html(html_text):
    tweets = []
    for article in re.findall(r'<div class="timeline-item"[^>]*>(.*?)</div>\s*</div>\s*</div>', html_text, re.DOTALL):
        content = re.search(r'<div class="content">(.*?)</div>\s*</div>', article, re.DOTALL)
        if not content: continue
        text = content.group(1)
        text = re.sub(r'<[^>]+>', ' ', text)
        text = html.unescape(re.sub(r'\s+', ' ', text).strip())
        if not text or len(text) < 10: continue
        author = "unknown"
        a = re.search(r'<a class="username"[^>]*>@(\w+)', article)
        if a: author = a.group(1)
        tweets.append({
            "source": "twitter", "author": author, "text": text[:500],
            "links": extract_links(text),
        })
    return tweets

def scrape_twitter(queries=None):
    if not requests: return []
    queries = queries or TWITTER_QUERIES
    found = []
    for q in queries:
        try:
            r = safe_get("https://nitter.net/search", params={"q": q, "f": "top"}, headers={"Accept": "text/html"})
            if not r: continue
            tweets = parse_nitter_html(r.text)
            for t in tweets: t["query"] = q
            found.extend(tweets)
            log(f"  Twitter '{q}': {len(tweets)} tweets")
            time.sleep(2)
        except: pass
    return found


# ═══════════════════════════════════════════════════════════════
# 4CHAN
# ═══════════════════════════════════════════════════════════════

CHAN_BOARDS = [
    ("g", "Technology"), ("sci", "Science & Math"), ("biz", "Business"),
    ("diy", "DIY"), ("gd", "Graphic Design"), ("ic", "Artwork/Critique"),
    ("mu", "Music"), ("int", "International"), ("3", "3DCG"),
]

def scrape_4chan(boards=None, max_threads=10):
    if not requests: return []
    boards = boards or CHAN_BOARDS
    found = []
    ai_keywords = re.compile(r'ai|llm|gpt|llama|diffusion|stable diffusion|flux|agent|rag|langchain|comfyui|open source|tool', re.I)
    for board, title in boards:
        try:
            r = safe_get(f"https://a.4cdn.org/{board}/catalog.json")
            if not r: continue
            pages = r.json()
            scanned = 0
            for page in pages:
                for thread in page.get("threads", []):
                    if scanned >= max_threads: break
                    sub = html.unescape(re.sub(r'<[^>]+>', '', thread.get("sub","") or ""))
                    com = html.unescape(re.sub(r'<[^>]+>', '', (thread.get("com","") or "")))[:500]
                    combined = sub + " " + com
                    if ai_keywords.search(combined):
                        found.append({
                            "source": "4chan", "board": board, "board_title": title,
                            "title": sub[:200], "text": com[:500],
                            "replies": thread.get("replies", 0), "thread_id": thread.get("no", 0),
                            "url": f"https://boards.4chan.org/{board}/thread/{thread.get('no',0)}",
                            "links": extract_links(combined),
                        })
                    scanned += 1
                if scanned >= max_threads: break
            log(f"  4chan /{board}/: AI threads")
            time.sleep(1)
        except: pass
    return found


# ═══════════════════════════════════════════════════════════════
# HACKER NEWS
# ═══════════════════════════════════════════════════════════════

def scrape_hackernews(max_stories=30):
    if not requests: return []
    try:
        r = safe_get("https://hn.algolia.com/api/v1/search",
                     params={"query": "AI", "tags": "story", "hitsPerPage": max_stories})
        if not r: return []
        data = r.json()
        found = []
        for hit in data.get("hits", []):
            title = hit.get("title", "")
            url = hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID','')}"
            found.append({
                "source": "hackernews", "title": title, "url": url,
                "points": hit.get("points", 0), "comments": hit.get("num_comments", 0),
            })
        log(f"  HN: {len(data.get('hits',[]))} stories")
        return found
    except: return []


# ═══════════════════════════════════════════════════════════════
# GITHUB
# ═══════════════════════════════════════════════════════════════

GITHUB_QUERIES = [
    ("AI tool", "stars:>100"), ("machine learning", "stars:>500"),
    ("LLM inference", "stars:>100"), ("AI agent", "stars:>100"),
]

def scrape_github(queries=None, per_query=10):
    if not requests: return []
    queries = queries or GITHUB_QUERIES
    found = []
    for term, qualifier in queries:
        try:
            q = urllib.parse.quote(f"{term} {qualifier}")
            r = safe_get(f"https://api.github.com/search/repositories?q={q}&sort=stars&order=desc&per_page={per_query}")
            if not r: continue
            data = r.json()
            for repo in data.get("items", []):
                full = repo.get("full_name", "")
                found.append({
                    "source": "github", "query": term,
                    "full_name": full, "description": (repo.get("description") or "")[:200],
                    "stars": repo.get("stargazers_count", 0), "language": repo.get("language", ""),
                    "url": repo.get("html_url", ""), "topics": repo.get("topics", []),
                })
            log(f"  GitHub '{term}': repos")
            time.sleep(2)
        except: pass
    return found


# ═══════════════════════════════════════════════════════════════
# OUTPUT
# ═══════════════════════════════════════════════════════════════

def deduplicate(results):
    seen = set()
    unique = []
    for r in results:
        src = r.get("source", "")
        key = r.get("full_name", "") or r.get("permalink", "") or r.get("url", "")
        if src == "twitter": key = r.get("author","") + r.get("text","")[:50]
        elif src == "4chan": key = f"{r.get('board','')}/{r.get('thread_id','')}"
        elif src == "hackernews": key = r.get("title","")
        elif src == "rss": key = r.get("title","") + r.get("feed","")
        if key and key not in seen:
            seen.add(key)
            unique.append(r)
    return unique

def save_results(results):
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M")
    filepath = OUTPUT_DIR / f"social_{ts}.json"

    by_source = {}
    for r in results:
        by_source.setdefault(r["source"], []).append(r)

    summary = f"# Social Discovery — {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}\n\n| Source | Items |\n|--------|-------|\n"
    for src, items in sorted(by_source.items()):
        summary += f"| {src} | {len(items)} |\n"
    summary += f"| **Total** | **{len(results)}** |\n"

    all_repos = {}
    for r in results:
        for link in r.get("links", []):
            if "/" in link:
                all_repos[link] = all_repos.get(link, 0) + 1

    if all_repos:
        summary += "\n## Discovered Repos\n\n| Repo | Mentions |\n|------|---------|\n"
        for repo, count in sorted(all_repos.items(), key=lambda x: -x[1])[:40]:
            summary += f"| [{repo}](https://github.com/{repo}) | {count} |\n"

    with open(filepath, "w") as f:
        json.dump({"timestamp": ts, "total": len(results),
                   "by_source": {k: len(v) for k,v in by_source.items()},
                   "repos": dict(sorted(all_repos.items(), key=lambda x: -x[1])[:50]),
                   "results": results}, f, indent=2, default=str)

    summary_path = filepath.with_suffix(".md")
    with open(summary_path, "w") as f: f.write(summary)

    log(f"Saved {len(results)} items to {filepath}")
    log(f"Summary: {summary_path}")
    return filepath


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    global OUTPUT_DIR, MAX_FEEDS_PER_RUN
    import argparse
    parser = argparse.ArgumentParser(description="Social Discovery Engine v2")
    parser.add_argument("--sources", default="all",
                       help="Comma-separated: rss,reddit,youtube,tiktok,twitter,chan,hn,github")
    parser.add_argument("--max-feeds", type=int, default=MAX_FEEDS_PER_RUN)
    parser.add_argument("--output-dir", default=str(OUTPUT_DIR))
    args = parser.parse_args()

    OUTPUT_DIR = Path(args.output_dir)
    MAX_FEEDS_PER_RUN = args.max_feeds
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if args.sources == "all":
        sources = ["rss", "reddit", "youtube", "tiktok", "twitter", "chan", "hn", "github"]
    else:
        sources = [s.strip() for s in args.sources.split(",")]

    if not requests:
        log("WARNING: requests not installed — HTTP sources disabled")
        sources = [s for s in sources if s not in ("rss","reddit","tiktok","twitter","chan","hn","github")]

    log(f"Social Discovery — sources: {', '.join(sources)}")
    start = time.time()

    scrapers = {
        "rss": scrape_rss,
        "reddit": scrape_reddit,
        "youtube": scrape_youtube,
        "tiktok": scrape_tiktok,
        "twitter": scrape_twitter,
        "chan": scrape_4chan,
        "hn": scrape_hackernews,
        "github": scrape_github,
    }

    all_results = []
    for src in sources:
        if src in scrapers:
            try:
                results = scrapers[src]()
                all_results.extend(results)
                log(f"  → {src}: {len(results)} items")
            except Exception as e:
                log(f"  ERROR {src}: {e}")

    all_results = deduplicate(all_results)
    filepath = save_results(all_results)

    elapsed = time.time() - start
    log(f"Done in {elapsed:.1f}s — {len(all_results)} unique items across {len(sources)} sources")
    print(f"\nResults: {filepath}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
