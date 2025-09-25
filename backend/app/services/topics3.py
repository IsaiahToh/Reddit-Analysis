from bertopic import BERTopic
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter
from itertools import chain
import re

docs = [
    "PC building costs are wild, GPUs still overpriced as hell.",
    "Anyone else trying out the new ChatGPT update? The responses feel way smoother ngl.",
    "Bro this AI coding assistant is cracked, wrote my whole Python function in seconds.",
    "Lowkey worried about AI taking over jobs tho… automation vibes everywhere.",
    "Man Elden Ring DLC is brutal af, bosses keep one-shotting me lol.",
    "Valorant patch dropped today, Sage wall feels nerfed again 😭.",
    "Anyone grinding ranked in League? Solo queue is actual pain rn.",
    "Crypto market pumping today, ETH breaking resistance finally 🚀.",
    "Bruh Tesla stock tanked after earnings, investors mad salty.",
    "New season of Stranger Things dropped!! The nostalgia hits so hard.",
    "Honestly the writing feels mid, but the soundtrack is straight fire 🔥.",
    "Discord vibes are toxic lately, Reddit feels dead rn.",
    "Netflix raising prices AGAIN, do they want me to pirate?",
    "PC building costs are wild, GPUs still overpriced as hell."
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
    ]

custom_stopwords = ["feels", "the","is","to","it","this","and","my","in","are","me","just","like","af","again","every", "a", "one", "so"]
vectorizer = CountVectorizer(stop_words=custom_stopwords, ngram_range=(1,2))
topic_model = BERTopic(vectorizer_model=vectorizer)
topics, probs = topic_model.fit_transform(docs)

print("\n=== Topics ===")
print(topic_model.get_topic_info())

def extract_lingo(posts, top_n=30):
    """
    Extract short trending phrases / slang from posts.
    - Uses unigrams + bigrams
    - Filters common stopwords
    """
    stopwords = set(custom_stopwords)
    tokenized = [re.findall(r"\b\w+\b", p.lower()) for p in posts]
    
    bigrams = [f"{w1} {w2}" for t in tokenized for w1, w2 in zip(t, t[1:])]
    
    freq = Counter(chain(*tokenized, bigrams))
    
    lingo = [k for k,v in freq.most_common(top_n) if k not in stopwords]
    return lingo

trending_lingo = extract_lingo(docs)
print("\n=== Trending Lingo ===")
print(trending_lingo)

def lingo_per_topic(posts, topics, top_n=10):
    topic_lingo = {}
    for t in set(topics):
        if t == -1:  
            continue
        topic_docs = [d for d, topic_id in zip(posts, topics) if topic_id == t]
        topic_lingo[t] = extract_lingo(topic_docs, top_n)
    return topic_lingo

topic_wise_lingo = lingo_per_topic(docs, topics)
print("\n=== Lingo per Topic ===")
for t, lingo in topic_wise_lingo.items():
    print(f"Topic {t}:", lingo)