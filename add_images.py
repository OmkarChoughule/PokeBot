import json

with open("pokemon_formatted_with_descriptions.json", "r") as f:
    data = json.load(f)

for i, pokemon in enumerate(data):
    dex_number = i + 1  # if order matches dex
    pokemon["image"] = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{dex_number}.png"
    pokemon["shiny"] = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/{dex_number}.png"
    

with open("pokemon_data_with_images.json", "w") as f:
    json.dump(data, f, indent=2)
