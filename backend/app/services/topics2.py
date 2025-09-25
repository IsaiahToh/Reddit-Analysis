import re
from bertopic import BERTopic
from keybert import KeyBERT
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

def clean_text(text):
    """Enhanced text cleaning for Reddit posts"""
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"[😭🚀💀🔥💎🙌😤👀💀😂]", "", text)
    text = re.sub(r"[!]{2,}", "!", text)  # Multiple ! to single !
    text = re.sub(r"[?]{2,}", "?", text)  # Multiple ? to single ?
    text = re.sub(r"[.]{3,}", "...", text)  # Multiple . to ...
    text = re.sub(r"\b\d{1,2}\b", "", text)  # Remove 1-2 digit numbers
    text = re.sub(r"\s+", " ", text).strip()
    return text

def remove_duplicates(docs):
    """Remove duplicate posts while preserving order"""
    seen = set()
    unique_docs = []
    for doc in docs:
        if doc not in seen:
            seen.add(doc)
            unique_docs.append(doc)
    return unique_docs

def filter_short_posts(docs, min_words=5):
    """Filter out very short posts"""
    return [doc for doc in docs if len(doc.split()) >= min_words]

docs = [
    "Anyone else trying out the new ChatGPT update? The responses feel way smoother ngl.",
    "Bro this AI coding assistant is cracked, wrote my whole Python function in seconds.",
    "Lowkey worried about AI taking over jobs tho… automation vibes everywhere.",
    "Man Elden Ring DLC is brutal af, bosses keep one-shotting me lol.",
    "Valorant patch dropped today, Sage wall feels nerfed again.",
    "Anyone grinding ranked in League? Solo queue is actual pain rn.",
    "Crypto market pumping today, ETH breaking resistance finally.",
    "Bruh Tesla stock tanked after earnings, investors mad salty.",
    "Anyone else dollar cost averaging into SPY? Feels like free money long-term.",
    "New season of Stranger Things dropped!! The nostalgia hits so hard.",
    "Honestly the writing feels mid, but the soundtrack is straight fire.",
    "Binge-watched in one night… sleep schedule = ruined lol.",
    "The new iPhone camera is insane, lowlight shots look professional.",
    "Why does every tech YouTuber keep hyping the same gadgets smh.",
    "Amazon delivery late AGAIN, kinda done with Prime tbh.",
    "Just finished Cyberpunk 2077 Phantom Liberty—fr tho, story >>> gameplay.",
    "Memecoins exploding rn, literally dog-themed tokens everywhere.",
    "Twitter feels dead since the last update, barely any engagement.",
    "Netflix raising prices AGAIN, do they want me to pirate?",
    "PC building costs are wild, GPUs still overpriced as hell.",
    "Steam sales got me again, backlog of games is officially infinite.",
    "Bruh Discord servers are so dry lately, no one chatting anymore.",
    "YouTube recommendations been weird af lately, random stuff popping up.",
    "Spotify keeps pushing the same playlists, discovery feels broken.",
    "Red Dead Redemption 2 still looks better than half the new releases.",
    "Cybersecurity job postings are everywhere, feels like the next gold rush.",
    "Amazon reviews are so fake now, can't trust anything.",
    "TikTok algorithm knows me better than my own friends.",
    "Google search results feel unusable now, just SEO spam all over.",
    "Wish GPUs would drop in price already, want to upgrade my rig.",
    "Metaverse hype died so fast, no one even talks about it anymore.",
    "Starfield performance is mid, optimization feels like Bethesda classic.",
    "AI voice cloning getting scary… heard a fake Drake song that fooled me.",
    "PS5 restocks are finally normal, remember the scalper era? Wild.",
    "Every crypto influencer is just shilling the same bags rn.",
    "Apple Vision Pro looks cool but 3.5k?? nah I'm good.",
    "Threads app had hype for like a week then silence lol.",
    "Zoom fatigue is real, can we go back to in-person pls.",
    "Meme stocks are back?? AMC and GME moving again.",
    "AI art debate never ends, some people love it, some hate it.",
    "Diablo 4 season feels like a grindfest, might drop it tbh.",
    "Pokemon Scarlet/Violet performance still trash, how??",
    "Snapchat AI feels useless, just gives me weird answers.",
    "FOMO hitting hard with everyone posting concert tickets.",
    "VRChat still underrated, funniest communities on there.",
    "Twitch ads are unbearable now, subbing feels mandatory.",
    "LinkedIn turning into Facebook with all the weird posts.",
    "Stonks only go up until they don't.",
    "AI-generated memes are everywhere, some are actually funny ngl.",
    "Fortnite collabs at this point are just wild, Eminem skin??",
    "Anime fandom discourse on Twitter is toxic af lately.",
    "Baldur's Gate 3 deserves GOTY, writing is next level.",
    "Every company suddenly has an AI chatbot now.",
    "Why does Uber Eats cost like double now… delivery fees insane.",
    "Discord Nitro not worth it anymore imo.",
    "Skyrim modding community carrying that game for a decade.",
    "YouTube Premium lowkey worth it just to skip ads.",
    "Payday 3 launch was rough, matchmaking barely works.",
    "Cybertruck sightings look so goofy on the road.",
    "Every Netflix original feels the same lately.",
    "Instagram reels are just recycled TikToks lol.",
    "Manga scans dropping before official release again.",
    "Literally everyone starting a podcast these days.",
    "Overwatch 2 still feels like OW1 but worse somehow.",
    "Reddit mods power tripping again, what's new.",
    "FIFA players stay toxic year after year.",
    "AirPods Pro noise cancelling is insane in crowded trains.",
    "Dark Souls fans never stop gatekeeping difficulty.",
    "AI essay detectors false flagging legit writing smh.",
    "Microtransactions killed gaming fr fr.",
    "Roblox devs making more money than indie studios.",
    "Every crypto winter feels the same, brutal lol.",
    "Subreddits going private after new API rules wild.",
    "Influencers selling scam courses again, nothing new.",
    "Mobile gaming ads are actual lies, different gameplay.",
    "Google Bard feels mid compared to ChatGPT.",
    "X (Twitter) just keeps getting worse every update.",
    "Gaming laptops still loud af, jet engine vibes.",
    "Kick streamers wilding with no TOS enforcement.",
    "GTA 6 leaks look insane, can't wait.",
    "E-scooter accidents everywhere in my city rn.",
    "OnlyFans discourse again on Reddit.",
    "AI dungeon stories getting unhinged lol.",
    "Windows 11 updates keep breaking stuff.",
    "Reddit gold feels useless now.",
    "Mobile battery life worse every year.",
    "NFT hype dead, nobody cares anymore.",
    "Spotify Wrapped season incoming soon.",
    "Why is gaming mouse inflation real??",
    "TikTok edits spoil every anime ending.",
    "Hogwarts Legacy drama everywhere still.",
    "Battle royale genre kinda dying ngl.",
    "Substack emails piling up, never read them.",
    "Why every tech CEO suddenly into meditation lol.",
    "CarPlay more reliable than half my car's UI.",
    "AI scam calls increasing, scary times.",
    "Diablo 2 remake still hits different.",
    "Discord AI features feel gimmicky af.",
    "VR headsets giving me headaches, anyone else?",
    "League toxic as ever, nothing changed.",
    "Cyberpunk anime adaptation was way better than expected."
]

def create_enhanced_topic_model():
    """Create an enhanced BERTopic model with better configuration"""
    
    custom_stopwords = [
        "the", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had",
        "do", "does", "did", "will", "would", "could", "should", "may", "might", "must",
        "can", "to", "of", "in", "for", "on", "with", "at", "by", "from", "up", "about",
        "into", "through", "during", "before", "after", "above", "below", "out", "off",
        "over", "under", "again", "further", "then", "once", "here", "there", "when",
        "where", "why", "how", "all", "any", "both", "each", "few", "more", "most",
        "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so",
        "than", "too", "very", "just", "now", "me", "my", "we", "our", "you", "your",
        "he", "his", "she", "her", "it", "its", "they", "their", "them",
        "af", "rn", "tbh", "imo", "smh", "lol", "ngl", "fr", "literally", "honestly", 
        "actually", "kinda", "gonna", "wanna", "gotta", "sorta", "pretty", "really",
        "super", "way", "like", "just", "still", "even", "also", "well", "good", 
        "better", "best", "right", "know", "think", "feel", "feels", "get", "got",
        "go", "goes", "going", "come", "comes", "coming", "take", "takes", "taking",
        "make", "makes", "making", "see", "sees", "seeing", "look", "looks", "looking",
        "want", "wants", "wanting", "need", "needs", "needing", "try", "tries", "trying",
        "use", "uses", "using", "work", "works", "working", "new", "old", "big", "small",
        "long", "short", "high", "low", "first", "last", "next", "previous", "every",
        "everyone", "everything", "everywhere", "anyone", "anything", "anywhere",
        "someone", "something", "somewhere", "nobody", "nothing", "nowhere"
    ]
    
    vectorizer = TfidfVectorizer(
        stop_words=custom_stopwords,
        ngram_range=(1, 3), 
        min_df=2,
        max_df=0.8,
        max_features=1000 
    )
    
    topic_model = BERTopic(
        vectorizer_model=vectorizer,
        min_topic_size=3,  
        nr_topics="auto", 
        calculate_probabilities=True, 
        verbose=True 
    )
    
    return topic_model

def create_enhanced_keybert():
    """Create enhanced KeyBERT model for better lingo extraction"""
    return KeyBERT()

def extract_enhanced_lingo(docs, topic_id, topics, kw_model):
    """Enhanced lingo extraction with MMR and filtering"""
    topic_docs = [d for d, t in zip(docs, topics) if t == topic_id]
    if not topic_docs:
        return []
    
    combined_text = " ".join(topic_docs)
    
    keywords = kw_model.extract_keywords(
        combined_text,
        keyphrase_ngram_range=(1, 3), 
        stop_words="english",
        use_mmr=True,  
        diversity=0.5,
        top_n=15
    )
    
    filtered_keywords = []
    for keyword, score in keywords:
        if (score > 0.3 and 
            len(keyword.split()) <= 2 and
            not any(generic in keyword.lower() for generic in 
                   ['new', 'good', 'better', 'best', 'great', 'nice', 'cool', 'bad', 'worse', 'worst'])):
            filtered_keywords.append(keyword)
    
    return filtered_keywords[:10]


def generate_topic_labels(topic_model, topics, filtered_posts):
    """Generate descriptive labels for topics based on keywords and content"""
    
    topic_patterns = {
        "Gaming": ["gaming", "game", "games", "valorant", "league", "elden", "ring", "cyberpunk", "diablo", 
                  "pokemon", "fortnite", "overwatch", "fifa", "dark", "souls", "baldur", "gate", "gta", 
                  "starfield", "payday", "skyrim", "ps5", "xbox", "nintendo", "steam", "epic", "bethesda",
                  "bosses", "nerfed", "grinding", "ranked", "solo", "queue", "matchmaking", "goty"],
        
        "AI & Technology": ["ai", "chatgpt", "artificial", "intelligence", "automation", "coding", "assistant", 
                           "python", "programming", "voice", "cloning", "generated", "memes", "essay", "detectors",
                           "bard", "openai", "machine", "learning", "algorithm", "tech", "technology"],
        
        "Cryptocurrency & Finance": ["crypto", "bitcoin", "eth", "ethereum", "memecoins", "tokens", "market", 
                                   "pumping", "tesla", "stock", "tanked", "earnings", "investors", "salty",
                                   "spy", "averaging", "stonks", "amc", "gme", "bags", "shilling", "winter", "brutal"],
        
        "Entertainment & Media": ["netflix", "stranger", "things", "writing", "soundtrack", "fire", "binge",
                                "watched", "sleep", "schedule", "youtube", "youtuber", "twitch", "ads", "subbing",
                                "spotify", "playlists", "discovery", "instagram", "reels", "tiktok", "manga",
                                "anime", "discord", "servers", "chatting"],
        
        "Tech Products & Reviews": ["iphone", "camera", "insane", "lowlight", "professional", "amazon", "delivery",
                                  "prime", "reviews", "fake", "apple", "vision", "pro", "airpods", "noise",
                                  "cancelling", "crowded", "trains", "cybertruck", "sightings", "goofy",
                                  "gaming", "laptops", "loud", "jet", "engine", "vibes", "gpus", "overpriced"],
        
        "Social Media & Platforms": ["twitter", "engagement", "threads", "app", "hype", "silence", "linkedin",
                                   "facebook", "weird", "posts", "reddit", "mods", "power", "tripping",
                                   "subreddits", "private", "api", "rules", "wild", "x", "getting", "worse"],
        
        "Work & Career": ["jobs", "automation", "vibes", "everywhere", "cybersecurity", "job", "postings",
                        "gold", "rush", "zoom", "fatigue", "person", "influencers", "selling", "scam",
                        "courses", "roblox", "devs", "money", "indie", "studios"],
        
        "Streaming & Content": ["netflix", "raising", "prices", "pirate", "youtube", "premium", "skip", "ads",
                               "twitch", "ads", "unbearable", "subbing", "mandatory", "kick", "streamers",
                               "wilding", "tos", "enforcement", "podcast", "days"]
    }
    
    labels = {}
    
    for topic_id in set(topics):
        if topic_id == -1:
            continue
            
        topic_words = [word for word, _ in topic_model.get_topic(topic_id)]
        topic_words_str = " ".join(topic_words).lower()
        
        best_category = "General Discussion"
        max_matches = 0
        
        for category, keywords in topic_patterns.items():
            matches = sum(1 for keyword in keywords if keyword in topic_words_str)
            if matches > max_matches:
                max_matches = matches
                best_category = category
        
        if best_category == "Gaming" and any(word in topic_words_str for word in ["valorant", "league", "elden"]):
            if "valorant" in topic_words_str or "league" in topic_words_str:
                best_category = "Gaming - Competitive"
            elif "elden" in topic_words_str or "cyberpunk" in topic_words_str:
                best_category = "Gaming - RPG"
        elif best_category == "AI & Technology" and "chatgpt" in topic_words_str:
            best_category = "AI - ChatGPT"
        elif best_category == "Cryptocurrency & Finance" and any(word in topic_words_str for word in ["crypto", "memecoins"]):
            best_category = "Crypto Trading"
        elif best_category == "Entertainment & Media" and "netflix" in topic_words_str:
            best_category = "Streaming Services"
        
        labels[f"Topic {topic_id}"] = best_category
    
    return labels

def extract_topics_and_lingo(posts):
    """Main function to extract topics and lingo from posts"""
    
    print("🔄 Preprocessing posts...")
    cleaned_posts = [clean_text(post) for post in posts]
    unique_posts = remove_duplicates(cleaned_posts)
    filtered_posts = filter_short_posts(unique_posts)
    
    print(f"📊 Processed {len(posts)} → {len(filtered_posts)} posts")
    
    print("🤖 Creating topic model...")
    topic_model = create_enhanced_topic_model()
    
    print("🔍 Fitting topics...")
    topics, probs = topic_model.fit_transform(filtered_posts)
    
    print("📋 Topic Overview:")
    topic_info = topic_model.get_topic_info()
    print(topic_info)
    
    print("\n🎯 Extracting lingo...")
    kw_model = create_enhanced_keybert()
    
    print("🏷️ Generating topic labels...")
    topic_labels = generate_topic_labels(topic_model, topics, filtered_posts)
    
    # Extract results
    results = {}
    for topic_id in set(topics):
        if topic_id == -1:  # Skip outliers
            continue
            
        topic_words = [word for word, _ in topic_model.get_topic(topic_id)]
        topic_lingo = extract_enhanced_lingo(filtered_posts, topic_id, topics, kw_model)
        
        # Count documents in topic
        doc_count = sum(1 for t in topics if t == topic_id)
        
        topic_key = f"Topic {topic_id}"
        results[topic_key] = {
            "doc_count": doc_count,
            "label": topic_labels.get(topic_key, "General Discussion"),
            "top_words": topic_words[:10],
            "lingo": topic_lingo
        }
    
    return results, topic_model

def display_results(results):
    """Display results in a formatted way with topic labels"""
    print("\n" + "="*50)
    print("🎯 TOPIC ANALYSIS RESULTS")
    print("="*50)
    
    for topic_name, data in results.items():
        label = data.get('label', 'General Discussion')
        print(f"\n📂 {topic_name}: {label} ({data['doc_count']} posts)")
        print("-" * 30)
        print(f"🔑 Top Words: {', '.join(data['top_words'])}")
        
        lingo_display = []
        for item in data['lingo']:
            if isinstance(item, tuple):
                lingo_display.append(f"{item[0]} ({item[1]:.3f})")
            else:
                lingo_display.append(str(item))
        print(f"🗣️  Trending Lingo: {', '.join(lingo_display[:10])}")

def extract_topics(posts, n_top_words=10):
    """API-compatible function for topic extraction"""
    results, _ = extract_topics_and_lingo(posts)
    topics = []
    for topic_name, data in results.items():
        topics.append(data['top_words'][:n_top_words])
    return topics

def extract_trending_lingo(posts, n_top_lingo=10):
    """API-compatible function for lingo extraction"""
    results, _ = extract_topics_and_lingo(posts)
    all_lingo = []
    for topic_name, data in results.items():
        all_lingo.extend(data['lingo'][:n_top_lingo])
    unique_lingo = list(dict.fromkeys(all_lingo))
    return unique_lingo[:n_top_lingo]

if __name__ == "__main__":
    print("🚀 Starting Enhanced Topic Analysis...")
    
    results, topic_model = extract_topics_and_lingo(docs)
    display_results(results)
    
    print(f"\n✅ Analysis complete! Found {len(results)} topics.")
