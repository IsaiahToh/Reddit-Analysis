from bertopic import BERTopic
from keybert import KeyBERT
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd

docs = [
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



def extract_topics(posts, n_topics=5, n_top_words=10):
    """Extract topics using BERTopic - standardized function"""
    from bertopic import BERTopic
    from sklearn.feature_extraction.text import CountVectorizer
    
    custom_stopwords = ["feels", "the","is","to","it","this","and","my","in","are","me","just","like","af","again","every", "a", "one", "so"]
    
    vectorizer = CountVectorizer(stop_words=custom_stopwords, ngram_range=(1, 2))
    
    topic_model = BERTopic(vectorizer_model=vectorizer)
    topics, probs = topic_model.fit_transform(posts)
    
    topics_list = []
    for topic_id in set(topics):
        if topic_id == -1:
            continue
        topic_words = [w for w, _ in topic_model.get_topic(topic_id)]
        topics_list.append(topic_words[:n_top_words])
    
    return topics_list

def extract_trending_lingo(posts, n_top_lingo=10):
    """Extract trending lingo using KeyBERT - standardized function"""
    from bertopic import BERTopic
    from sklearn.feature_extraction.text import CountVectorizer
    
    custom_stopwords = ["feels", "the","is","to","it","this","and","my","in","are","me","just","like","af","again","every", "a", "one", "so"]
    
    vectorizer = CountVectorizer(stop_words=custom_stopwords, ngram_range=(1, 2))
    
    topic_model = BERTopic(vectorizer_model=vectorizer)
    topics, probs = topic_model.fit_transform(posts)
    
    kw_model = KeyBERT()
    
    all_lingo = []
    for topic_id in set(topics):
        if topic_id == -1:
            continue
        topic_docs = [d for d, t in zip(posts, topics) if t == topic_id]
        if topic_docs:
            keywords = kw_model.extract_keywords(
                topic_docs,
                keyphrase_ngram_range=(1, 2),
                stop_words="english",
                top_n=5
            )
            all_lingo.extend([k[0] for k in keywords])
    
    unique_lingo = list(dict.fromkeys(all_lingo))
    return unique_lingo[:n_top_lingo]

if __name__ == "__main__":
    print("🚀 Testing BERTopic + KeyBERT Analysis...")
    
    topics = extract_topics(docs)
    print("Extracted Topics:")
    for idx, topic_words in enumerate(topics):
        print(f"Topic {idx + 1}: {', '.join(topic_words)}")
    
    lingo = extract_trending_lingo(docs)
    print("Trending Lingo:")
    print(", ".join(lingo))
