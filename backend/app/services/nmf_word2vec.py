
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from sklearn.cluster import KMeans
from gensim.models import Word2Vec
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from collections import Counter
import numpy as np

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+", "", text) # remove URLs
    text = re.sub(r"[^a-z\s]", "", text) # remove punctuation/numbers
    text = re.sub(r"\s+", " ", text).strip() # remove extra spaces
    return text

def clean_and_tokenize(text):
    text = clean_text(text)
    return [word for word in simple_preprocess(text) if word not in STOPWORDS]

def extract_topics(posts, n_topics=3, n_top_words=10):
    cleaned_posts = [clean_text(post) for post in posts]

    tfidf_vectorizer = TfidfVectorizer(max_df=0.5, min_df=2, stop_words='english', ngram_range=(1,2))
    X_tfidf = tfidf_vectorizer.fit_transform(cleaned_posts)

    nmf = NMF(n_components=n_topics, random_state=42)
    nmf_features = nmf.fit_transform(X_tfidf)
    feature_names = tfidf_vectorizer.get_feature_names_out()
    topics = []
    for topic_idx, topic in enumerate(nmf.components_):
        top_words = [feature_names[i] for i in topic.argsort()[-n_top_words:][::-1]]
        topics.append(top_words)
    return topics

def extract_trending_lingo(posts, n_clusters=None, n_top_lingo=5):
    cleaned_posts = [clean_text(post) for post in posts]
    tokenized_posts = [clean_and_tokenize(post) for post in cleaned_posts]
    w2v_model = Word2Vec(
        sentences=tokenized_posts,
        vector_size=200,
        window=5,
        min_count=2,
        workers=4,
        sg=1,
        epochs=20
    )

    words = list(w2v_model.wv.index_to_key)
    word_vectors = np.array([w2v_model.wv[word] for word in words])
    if n_clusters is None:
        n_clusters = max(2, int(np.sqrt(len(words))))
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(word_vectors)
    labels = kmeans.labels_
    cluster_to_words = {}
    for word, label in zip(words, labels):
        cluster_to_words.setdefault(label, []).append(word)

    token_flat = [word for sentence in tokenized_posts for word in sentence]
    word_counts = Counter(token_flat)
    trending_lingo = []
    for cluster_words in cluster_to_words.values():
        sorted_words = sorted(cluster_words, key=lambda w: word_counts[w], reverse=True)
        trending_lingo.extend(sorted_words[:n_top_lingo])
    
    trending_lingo = list(dict.fromkeys(trending_lingo))
    return trending_lingo

if __name__ == "__main__":
    scraped_posts = [
        "Anyone else trying out the new ChatGPT update? The responses feel way smoother ngl.",
        "Bro this AI coding assistant is cracked, wrote my whole Python function in seconds.",
        "Lowkey worried about AI taking over jobs tho… automation vibes everywhere.",
        "Man Elden Ring DLC is brutal af, bosses keep one-shotting me lol.",
        "Valorant patch dropped today, Sage wall feels nerfed again 😭.",
        "Anyone grinding ranked in League? Solo queue is actual pain rn.",
        "Crypto market pumping today, ETH breaking resistance finally 🚀.",
        "Bruh Tesla stock tanked after earnings, investors mad salty.",
        "Anyone else dollar cost averaging into SPY? Feels like free money long-term.",
        "New season of Stranger Things dropped!! The nostalgia hits so hard.",
        "Honestly the writing feels mid, but the soundtrack is straight fire 🔥.",
        "Binge-watched in one night… sleep schedule = ruined lol.",
        "The new iPhone camera is insane, lowlight shots look professional.",
        "Why does every tech YouTuber keep hyping the same gadgets smh.",
        "Amazon delivery late AGAIN, kinda done with Prime tbh.",
        "Just finished Cyberpunk 2077 Phantom Liberty—fr tho, story >>> gameplay.",
        "Memecoins exploding rn, literally dog-themed tokens everywhere 😂.",
        "Twitter feels dead since the last update, barely any engagement.",
        "Netflix raising prices AGAIN, do they want me to pirate?",
        "PC building costs are wild, GPUs still overpriced as hell.",
        "Steam sales got me again, backlog of games is officially infinite.",
        "Bruh Discord servers are so dry lately, no one chatting anymore.",
        "YouTube recommendations been weird af lately, random stuff popping up.",
        "Spotify keeps pushing the same playlists, discovery feels broken.",
        "Red Dead Redemption 2 still looks better than half the new releases.",
        "Cybersecurity job postings are everywhere, feels like the next gold rush.",
        "Amazon reviews are so fake now, can’t trust anything 😤.",
        "TikTok algorithm knows me better than my own friends.",
        "Google search results feel unusable now, just SEO spam all over.",
        "Wish GPUs would drop in price already, want to upgrade my rig.",
        "Metaverse hype died so fast, no one even talks about it anymore.",
        "Starfield performance is mid, optimization feels like Bethesda classic.",
        "AI voice cloning getting scary… heard a fake Drake song that fooled me.",
        "PS5 restocks are finally normal, remember the scalper era? Wild.",
        "Every crypto influencer is just shilling the same bags rn.",
        "Apple Vision Pro looks cool but 3.5k?? nah I’m good.",
        "Threads app had hype for like a week then silence lol.",
        "Zoom fatigue is real, can we go back to in-person pls.",
        "Meme stocks are back?? AMC and GME moving again 💎🙌.",
        "AI art debate never ends, some people love it, some hate it.",
        "Diablo 4 season feels like a grindfest, might drop it tbh.",
        "Pokemon Scarlet/Violet performance still trash, how??",
        "Snapchat AI feels useless, just gives me weird answers.",
        "FOMO hitting hard with everyone posting concert tickets.",
        "VRChat still underrated, funniest communities on there.",
        "Twitch ads are unbearable now, subbing feels mandatory.",
        "LinkedIn turning into Facebook with all the weird posts.",
        "Stonks only go up until they don’t 💀.",
        "AI-generated memes are everywhere, some are actually funny ngl.",
        "Fortnite collabs at this point are just wild, Eminem skin??",
        "Anime fandom discourse on Twitter is toxic af lately.",
        "Baldur’s Gate 3 deserves GOTY, writing is next level.",
        "Every company suddenly has an AI chatbot now.",
        "Why does Uber Eats cost like double now… delivery fees insane.",
        "Discord Nitro not worth it anymore imo.",
        "Skyrim modding community carrying that game for a decade.",
        "YouTube Premium lowkey worth it just to skip ads.",
        "Payday 3 launch was rough, matchmaking barely works.",
        "Cybertruck sightings look so goofy on the road 😂.",
        "Every Netflix original feels the same lately.",
        "Instagram reels are just recycled TikToks lol.",
        "Manga scans dropping before official release again 👀.",
        "Literally everyone starting a podcast these days.",
        "Overwatch 2 still feels like OW1 but worse somehow.",
        "Reddit mods power tripping again, what’s new.",
        "FIFA players stay toxic year after year.",
        "AirPods Pro noise cancelling is insane in crowded trains.",
        "Dark Souls fans never stop gatekeeping difficulty.",
        "AI essay detectors false flagging legit writing smh.",
        "Microtransactions killed gaming fr fr.",
        "Roblox devs making more money than indie studios.",
        "Every crypto winter feels the same, brutal lol.",
        "Subreddits going private after new API rules wild.",
        "Influencers selling scam courses again, nothing new.",
        "Mobile gaming ads are actual lies, different gameplay 💀.",
        "Google Bard feels mid compared to ChatGPT.",
        "X (Twitter) just keeps getting worse every update.",
        "Gaming laptops still loud af, jet engine vibes.",
        "Kick streamers wilding with no TOS enforcement.",
        "GTA 6 leaks look insane, can’t wait.",
        "E-scooter accidents everywhere in my city rn.",
        "OnlyFans discourse again on Reddit 💀.",
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
        "CarPlay more reliable than half my car’s UI.",
        "AI scam calls increasing, scary times.",
        "Diablo 2 remake still hits different.",
        "Discord AI features feel gimmicky af.",
        "VR headsets giving me headaches, anyone else?",
        "League toxic as ever, nothing changed.",
        "Cyberpunk anime adaptation was way better than expected."
    ]

    topics = extract_topics(scraped_posts)
    print("Extracted Topics:")
    for idx, topic_words in enumerate(topics):
        print(f"Topic {idx + 1}: {', '.join(topic_words)}")
    trending_lingo = extract_trending_lingo(scraped_posts)
    print("Top Trending Lingo / Phrases:")
    print(", ".join(trending_lingo))
