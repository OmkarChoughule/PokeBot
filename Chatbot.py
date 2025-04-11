import json
import random
import spacy
from rapidfuzz import process

# Load spaCy NLP
nlp = spacy.load("en_core_web_sm")

with open("pokemon_data_with_images.json", "r") as f:
    pokedex = json.load(f)

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

    # Step 1: Try exact match
    if name in pokemon_dict:
        return pokemon_dict[name]

    # Step 2: Try fuzzy match
    best_match, score, _ = process.extractOne(name, all_names)
    print(f"[DEBUG] Matched '{name}' to '{best_match}' with score {score}")
    
    if score > 90:  # Tighten threshold to avoid bad guesses
        return pokemon_dict.get(best_match)

    # Optional: Give user feedback if the match is weak
    return None

def extract_pokemon_names(text,id=0):
    if id ==1:
        doc = nlp(text)
        candidates = [token.text.lower() for token in doc if token.is_alpha]
        found = []
        for word in candidates:
            match, score, _ = process.extractOne(word, all_names)
            if score > 90:
                found.append(match)
        return list(set(found)) 

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
    return [t for t, val in pokemon["type_effectiveness"].items() if val < 1.0 and val != 0.0]

def get_immunities(pokemon):
    return [t for t, val in pokemon["type_effectiveness"].items() if val == 0.0]

# ---------- Response Templates ----------

def describe_pokemon(p):
    stats = p["base_stats"]
    abilities = p.get("abilities", [])
    ability_descs = p.get("abilityDescriptions", [])
    types = get_type_emoji(p.get("types", []))
    image_url = p.get("image", "Image not available")
    shiny_url = p.get("shiny", "Shiny not available")

    abilities_full = "\n".join(
        f"- {name}: {desc}" for name, desc in zip(abilities, ability_descs)
    )

    return f"""
🖼️ Normal: <img src="{image_url}" alt="{p['name']}" width="150">
<br>
🌟 Shiny: <img src="{shiny_url}" alt="{p['name']} Shiny" width="150">
✨ {p['name']} — {types}
📖 {p['description']}

🔢 Stats:
HP: {stats['hp']}, Atk: {stats['attack']}, Def: {stats['defense']}
Sp. Atk: {stats['sp_atk']}, Sp. Def: {stats['sp_def']}, Speed: {stats['speed']}

🧬 Abilities:
{abilities_full}

🌟 Legendary: {'Yes' if p['meta']['is_legendary'] else 'No'}, Gen: {p['meta']['generation']}
""".strip()


def compare_pokemon(p1, p2):
    stats = ["hp", "attack", "defense", "sp_atk", "sp_def", "speed"]
    result = [f"📊 Comparing {p1['name']} vs {p2['name']}"]

    for stat in stats:
        val1, val2 = p1["base_stats"][stat], p2["base_stats"][stat]
        better = "Tie" if val1 == val2 else p1["name"] if val1 > val2 else p2["name"]
        result.append(f"{stat.upper()}: {val1} vs {val2} → {better}")

    return "\n".join(result)

# ---------- Bot Core ----------

def handle_query(query):
    query = query.lower()
    if "random" in query or "surprise" in query:
        return describe_pokemon(random.choice(list(pokemon_dict.values())))

    names = extract_pokemon_names(query)

    if any(w in query for w in ["compare", "vs", "versus", "better", "stronger", "and"]) and len(names) >= 2:
        p1, p2 = find_pokemon(names[0]), find_pokemon(names[1])
        if p1 and p2:
            return compare_pokemon(p1, p2)
        else:
            return "One of those Pokémon names wasn't recognized."

    if any(w in query for w in ["weak","weakness", "resist", "resistance", "immune", "immunity", "immunities", "battle"]):
        if names:
            poke = find_pokemon(names[0])
            if poke:
                weak = get_weaknesses(poke)
                resist = get_resistances(poke)
                immune = get_immunities(poke)
                return (
                    f"{poke['name']} is weak to: {', '.join(weak) or 'None'}\n"
                    f"And resistant to: {', '.join(resist) or 'None'}\n"
                    f"And immune to: {', '.join(immune) or 'None'}"
                )
        return "I couldn't find that Pokémon."
    if any(w in query for w in ["tell","me","about","what","give","info","information"]):
        names = extract_pokemon_names(query,1)
        if names:
            poke = find_pokemon(names[0])
            if poke:
                return describe_pokemon(poke)

        return "Hmm... I didn’t catch that. Try asking about a Pokémon or type 'random'!"
    
    if names:
            poke = find_pokemon(names[0])
            if poke:
                return describe_pokemon(poke)

    return "Hmm... I didn’t catch that. Try asking about a Pokémon or type 'random'!"

# ---------- CLI ----------

if __name__ == "__main__":
    print("🎮 Welcome to PokéBot! Ask me anything. Type 'exit' to leave.\n")

    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in ["exit", "quit"]:
            print("Bot: Smell ya later! 👋")
            break
        response = handle_query(user_input)
        print(f"Bot: {response}\n")
