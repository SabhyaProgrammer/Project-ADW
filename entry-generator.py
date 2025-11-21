# ...existing code...
import json
import os
from typing import Dict, List
import random
import sys
# ...existing code...

class HerbInventory:
    # ...existing code...

    def generate_sample_data(self, count: int = 100, seed: int | None = None):
        """
        Generate `count` sample herb entries with anime isekai styled names and locations.
        This replaces current in-memory list with generated items and saves to disk.
        Call with: inventory.generate_sample_data(100)
        """
        if seed is not None:
            random.seed(seed)

        prefixes = [
            "Astra", "Lumi", "Ether", "Myth", "Nexa", "Sylph", "Auri", "Verdi", "Kage", "Runa",
            "Yomi", "Hikari", "Sora", "Fen", "Zera", "Kiria", "Orion", "Noct", "Mira", "Gale"
        ]
        middles = [
            "veil", "bloom", "crystal", "shade", "song", "heart", "stone", "glow", "spark", "root"
        ]
        suffixes = [
            "leaf", "petal", "bark", "seed", "dust", "tea", "moss", "stem", "tear", "root"
        ]
        loc_prefix = [
            "Kingdom of", "Forest of", "Isle of", "Skyrealm of", "Valley of", "Empire of",
            "Cavern of", "Tower of", "Plains of", "Sanctuary of"
        ]
        loc_names = [
            "Elysium", "Abyss", "Arcanum", "Verdantia", "Lunaria", "Nexus", "Regalia",
            "Driftwood", "Silvermist", "Crimson Hollow", "Glimmerfen", "Starfall", "Twilight"
        ]

        generated = []
        seen = set()
        idx = 1
        while len(generated) < count:
            name = f"{random.choice(prefixes)}{random.choice(middles).capitalize()}{random.choice(suffixes).capitalize()}"
            # ensure some uniqueness
            if name in seen:
                name = f"{name} {idx}"
            seen.add(name)

            location = f"{random.choice(loc_prefix)} {random.choice(loc_names)}"
            price = round(random.uniform(0.5, 250.0), 2)  # realistic price range

            generated.append({
                "name": name,
                "price": price,
                "location": location
            })
            idx += 1

        # replace current list with generated data and persist
        self.herbs = generated
        try:
            self.save_data()
            print(f"Generated {len(generated)} sample herbs and saved to {self.filename}")
        except Exception as e:
            print(f"Could not save generated data: {e}")

# ...existing code...

if __name__ == "__main__":
    # support a quick CLI switch to generate sample data without running the interactive menu
    if len(sys.argv) > 1 and sys.argv[1] in ("--generate-sample", "--gen-sample"):
        inv = HerbInventory()
        count = 100
        seed = 42
        # allow overriding count via second arg
        if len(sys.argv) > 2:
            try:
                count = int(sys.argv[2])
            except Exception:
                pass
        if len(sys.argv) > 3:
            try:
                seed = int(sys.argv[3])
            except Exception:
                seed = 42

        inv.generate_sample_data(count=count, seed=seed)
        input("Sample generation complete. Press Enter to exit...")
    else:
        main()
# ...existing code...
