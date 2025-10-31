import re                       #python regular expression(A-Z,a-z,0-9,apostrophes,.....)
from collections import Counter #counting the occurances

#regular expression: finding all sequence word entered: A-z, a-z,'
WORD_RE = re.compile(r"[A-Za-z']+") #+ tells to keep going until any unrecoganised object found then stop and again continue

def analyze_text_safety(text): #takes scrapped text as input and check

    #analyze the text for unsafe or sensitive content, can be added more
    UNSAFE_WORDS = {
        "violence": [
            "kill", "murder", "attack", "bomb", "terror", "war", "shoot", "stab",
            "massacre", "slaughter", "assault", "execute", "terrorist"
        ],
        "abuse": [
            "hate", "idiot", "stupid", "dumb", "trash", "moron", "fool",
            "retard", "loser", "bastard", "jerk"
        ],
        "obscene": [
            "fuck", "fucking", "fucked", "shit", "bitch", "bastard", "whore",
            "asshole", "cum", "dick", "pussy", "cunt"
        ],
        "drugs": [
            "cocaine", "heroin", "meth", "mushroom", "lsd", "weed", "marijuana",
            "opioid", "amphetamine", "drug", "smack"
        ],
        "tech_threat": [
            "virus", "trojan", "worm", "malware", "ransomware", "exploit", "backdoor",
            "phishing", "spyware", "botnet", "attack", "ddos"
        ],
        "hate_against_groups": [
            "racist", "nazi", "kill the", "all muslims", "all jews", "hate muslims",
            "hate jews", "hate blacks", "hate indians"
        ],
        "sex_trafficking": [
            "human trafficking", "sex trafficking", "traffick", "pimp", "escort",
            "sexual exploitation"
        ],
        "self_harm": [
            "suicide", "kill myself", "self-harm", "cutting", "hang myself"
        ]
    }

    # Flatten all unsafe words for quick lookup
    FLATTENED = set()   #making a set of unsafe words without taking duplicating
    for words in UNSAFE_WORDS.values(): #values under the categories created
        for w in words:
            if " " not in w:  # only single words not in, eliminating spacings
                FLATTENED.add(w.lower()) #adding to the set in lowercase

    if not text:
        return None

    tokens = [m.group(0).lower() for m in WORD_RE.finditer(text)] #finds all the matchings m, and group them in lowercase
    total_words = len(tokens)   #count
    category_counts = {catg: 0 for catg in UNSAFE_WORDS}  #stores words according to the category
    matched_examples = {catg: Counter() for catg in UNSAFE_WORDS} #stores number of occurances of the word

    joined = " ".join(tokens)  #joining the tokens with single space
    unsafe_hits = 0             #initial


    #looping through the unsafe words dict and the words itself
    for catg, words in UNSAFE_WORDS.items():
        for w in words:       #going through undsafe words inside unsafe category
            if " " in w:      #ensures spacing (only look for multi word unsafe phases)
                count = joined.count(w.lower()) #count the word occurance
                if count > 0:
                    category_counts[catg] += count #multiple category word count
                    matched_examples[catg][w] += count  #word or phase appeared how many times
                    unsafe_hits += count

    # Single word detection
    for token in tokens:
        if token in FLATTENED:
            for catg, words in UNSAFE_WORDS.items():
                if token in [x.lower() for x in words]: #each category is in normalised lowecase
                    category_counts[catg] += 1  #count of unsafe words
                    matched_examples[catg][token] += 1 #category wise token count
                    unsafe_hits += 1

    #score calculation
    #100.0 - (unsafe_hits / total_words * 100.0): unsafe calculation
    safety_score = 100.0 if total_words == 0 else max(0.0, 100.0 - (unsafe_hits / total_words * 100.0))

    result = {
        'total_words': total_words,
        'unsafe_hits': unsafe_hits,
        'safety_score': round(safety_score, 2),
        'category_counts': category_counts,
        'matched_examples': {
            catg: dict(cnt.most_common(10))
            for catg, cnt in matched_examples.items()
        }
    }

    return result
