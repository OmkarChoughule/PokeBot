import json
import requests
import time

# Load your Pokémon JSON file
with open("pokemon_formatted.json", "r", encoding="utf-8") as file:
    pokemon_data = json.load(file)

def get_pokedex_description(name):
    url = f"https://pokeapi.co/api/v2/pokemon-species/{name.lower()}"
    response = requests.get(url)
    if response.status_code != 200:
        return "No description found."
    
    data = response.json()
    for entry in data["flavor_text_entries"]:
        if entry["language"]["name"] == "en":
            return entry["flavor_text"].replace("\n", " ").replace("\x0c", " ")
    return "No description available."

def get_ability_description(ability):
    url = f"https://pokeapi.co/api/v2/ability/{ability.lower()}"
    response = requests.get(url)
    if response.status_code != 200:
        return "No ability description found."
    
    data = response.json()
    for entry in data["effect_entries"]:
        if entry["language"]["name"] == "en":
            return entry["short_effect"]
    return "No ability description available."

# Cache to avoid duplicate API calls
ability_cache = {}

# Loop through Pokémon
for p in pokemon_data:
    name = p["name"]
    print(f"Fetching {name}...")

    # Description
    p["description"] = get_pokedex_description(name)
    
    # Abilities
    p["abilityDescriptions"] = []
    for ability in p.get("abilities", []):
        if ability not in ability_cache:
            ability_cache[ability] = get_ability_description(ability)
            time.sleep(0.5)  # avoid rate limits
        p["abilityDescriptions"].append(ability_cache[ability])
    
    time.sleep(0.5)  # avoid rate limits

# Save the enriched file
with open("pokemon_formatted_with_descriptions.json", "w", encoding="utf-8") as out_file:
    json.dump(pokemon_data, out_file, indent=2)

print("✅ All descriptions added and file saved.")
