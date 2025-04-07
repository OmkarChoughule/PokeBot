import pandas as pd
import json

# Load the CSV
df = pd.read_csv("pokemon.csv")

# Fill NaNs for type2 and abilities
df["type2"] = df["type2"].fillna("")
df["abilities"] = df["abilities"].apply(eval)  # convert string list to real list

# Final list to store cleaned Pokémon entries
formatted_pokemon = []

for _, row in df.iterrows():
    entry = {
        "name": row["name"],
        "types": [row["type1"]] + ([row["type2"]] if row["type2"] else []),
        "abilities": row["abilities"],
        "base_stats": {
            "hp": int(row["hp"]),
            "attack": int(row["attack"]),
            "defense": int(row["defense"]),
            "sp_atk": int(row["sp_attack"]),
            "sp_def": int(row["sp_defense"]),
            "speed": int(row["speed"]),
        },
        "meta": {
            "generation": int(row["generation"]),
            "is_legendary": bool(row["is_legendary"])
        },
        "type_effectiveness": {
            key.replace("against_", ""): float(row[key])
            for key in row.index if key.startswith("against_")
        }
    }

    formatted_pokemon.append(entry)

# Save to JSON
with open("pokemon_formatted1.json", "w") as f:
    json.dump(formatted_pokemon, f, indent=2)
