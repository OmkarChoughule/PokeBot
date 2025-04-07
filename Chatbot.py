import json
import random
import spacy
from rapidfuzz import process

# Load spaCy NLP
nlp = spacy.load("en_core_web_sm")

# Load JSON data
with open("pokemon_formatted.json", "r") as f:
    pokedex = json.load(f)

# Build name-to-data map
pokemon_dict = {p["name"].lower(): p for p in pokedex}
all_names = list(pokemon_dict.keys())

# Type → Emoji mapping
type_emojis = {
    "Fire": "🔥", "Water": "💧", "Grass": "🌿", "Electric": "⚡", "Psychic": "🧠",
    "Flying": "🕊️", "Bug": "🐛", "Poison": "☠️", "Normal": "✨", "Ghost": "👻",
    "Dragon": "🐉", "Ice": "❄️", "Rock": "🪨", "Steel": "🛡️", "Dark": "🌑",
    "Fairy": "🧚", "Ground": "🌍", "Fighting": "🥊"
}

# ---------- Utilities ----------

def find_pokemon(name):
    name = name.lower()
    if name in pokemon_dict:
        return pokemon_dict[name]
    match, score, _ = process.extractOne(name, all_names)
    return pokemon_dict[match] if score > 75 else None

def extract_pokemon_names(text):
    doc = nlp(text)
    candidates = [token.text.lower() for token in doc if token.is_alpha]
    found = []
    for word in candidates:
        match, score, _ = process.extractOne(word, all_names)
        if score > 85:
            found.append(match)
    return list(set(found))

def get_type_emoji(types):
    return " ".join([f"{t.capitalize()} {type_emojis.get(t.capitalize(), '')}" for t in types])

def get_weaknesses(pokemon):
    return [t for t, val in pokemon["type_effectiveness"].items() if val > 1.0]

def get_resistances(pokemon):
    return [t for t, val in pokemon["type_effectiveness"].items() if val < 1.0]

# ---------- Response Templates ----------

def describe_pokemon(p):
    stats = p["base_stats"]
    types = get_type_emoji(p["types"])
    abilities = ", ".join(p["abilities"])
    return f"""
✨ {p['name']} — {types}
HP: {stats['hp']}, Atk: {stats['attack']}, Def: {stats['defense']}
Sp. Atk: {stats['sp_atk']}, Sp. Def: {stats['sp_def']}, Speed: {stats['speed']}
Abilities: {abilities}
Legendary: {'Yes' if p['meta']['is_legendary'] else 'No'}, Gen: {p['meta']['generation']}
""".strip()

def compare_pokemon(p1, p2):
    stats = ["hp", "attack", "defense", "sp_atk", "sp_def", "speed"]
    lines = [f"📊 Comparing {p1['name']} vs {p2['name']}"]
    for stat in stats:
        a = p1["base_stats"][stat]
        b = p2["base_stats"][stat]
        winner = "Tie" if a == b else p1["name"] if a > b else p2["name"]
        lines.append(f"{stat.upper()}: {a} vs {b} → {winner}")
    return "\n".join(lines)

# ---------- Bot Core ----------

def handle_query(query):
    query = query.lower()

    if "random" in query or "surprise" in query:
        return describe_pokemon(random.choice(list(pokemon_dict.values())))

    names = extract_pokemon_names(query)

    if any(w in query for w in ["compare", "vs", "versus", "better", "stronger"]) and len(names) >= 2:
        p1, p2 = find_pokemon(names[0]), find_pokemon(names[1])
        if p1 and p2:
            return compare_pokemon(p1, p2)
        else:
            return "One of those Pokémon names wasn't recognized."

    if any(w in query for w in ["weak", "resist", "resistance"]):
        if names:
            poke = find_pokemon(names[0])
            if poke:
                weak = get_weaknesses(poke)
                resist = get_resistances(poke)
                return (
                    f"{poke['name']} is weak to: {', '.join(weak) or 'None'}\n"
                    f"And resistant to: {', '.join(resist) or 'None'}"
                )
        return "I couldn't find that Pokémon."

    if names:
        poke = find_pokemon(names[0])
        if poke:
            return describe_pokemon(poke)

    return "Hmm... I didn’t catch that. Try asking about a Pokémon or type 'random'!"

# ---------- CLI ----------

print("🎮 Welcome to PokéBot! Ask me anything. Type 'exit' to leave.\n")

while True:
    user_input = input("You: ")
    if user_input.strip().lower() in ["exit", "quit"]:
        print("Bot: Smell ya later! 👋")
        break
    response = handle_query(user_input)
    print(f"Bot: {response}\n")
