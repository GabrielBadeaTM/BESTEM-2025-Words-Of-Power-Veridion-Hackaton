import numpy as np

# ======================
# Functie pentru incarcare GloVe
# ======================
def load_glove_embeddings(filepath):
    print("Se incarca embeddings din fisier...")
    embeddings = {}
    with open(filepath, 'r', encoding='utf8') as f:
        for line in f:
            parts = line.strip().split()
            word = parts[0]
            vector = np.array(parts[1:], dtype=float)
            embeddings[word] = vector
    print(f"Am incarcat {len(embeddings)} cuvinte.")
    return embeddings

# ======================
# Functie pentru calculare similaritate cosinus
# ======================
def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    return dot_product / (norm1 * norm2)

# ======================
# Functie pentru a calcula vectorul mediu al unei categorii sau expresii
# ======================
def average_vector(words, embeddings):
    vectors = []
    for word in words:
        if word in embeddings:
            vectors.append(embeddings[word])
        else:
            print(f"Atentie: '{word}' nu exista in embeddings.")
    if vectors:
        return np.mean(vectors, axis=0)
    else:
        return None

# ======================
# Functie pentru clasificarea unui cuvant sau expresie in cea mai apropiata categorie
# ======================
def classify_tool(word_or_phrase, embeddings, categories_vectors):
    words = word_or_phrase.lower().split()
    vectors = []
    for w in words:
        if w in embeddings:
            vectors.append(embeddings[w])
        else:
            print(f"Atentie: Cuvantul '{w}' nu exista in embeddings!")
    if not vectors:
        print(f"Nu s-a gasit niciun vector pentru '{word_or_phrase}'.")
        return None
    word_vec = np.mean(vectors, axis=0)

    max_similarity = -1
    best_category = None

    for category, category_vec in categories_vectors.items():
        similarity = cosine_similarity(word_vec, category_vec)
        if similarity > max_similarity:
            max_similarity = similarity
            best_category = category

    print(f"\n'{word_or_phrase}' este cel mai vulnerabil la: {best_category} (similaritate: {max_similarity:.4f})")
    return best_category

# ======================
# MAIN PROGRAM
# ======================
if __name__ == "__main__":
    # 1. Incarcam embeddings
    glove_path = "glove.6B.200d.txt"  # Asigura-te ca este calea corecta
    embeddings = load_glove_embeddings(glove_path)

    # 2. Definim uneltele si vulnerabilitatile lor
    tools_categories = {
        "Sandpaper": [
            # Suprafețe și materiale de bază
            "rust", "surface", "paint", "wood", "paper", "plastic", "leather", "painting", "varnish", "coating",
            "oxidation", "corrosion", "patina", "edge", "splinter", "uneven", "rough", "scratched",
            
            # Metale și finisaje metalice
            "tarnished", "silver", "weathered", "bronze", "oxidized", "copper", "rusted", "iron", "corroded", "aluminum", 
            "aged", "brass", "dull", "chrome", "spotted", "nickel", "faded", "gold", "leaf", "platinum", 
            "blackened", "steel", "pitted", "zinc", "discolored", "titanium", "sculpture", "statue", "armor", "coins",
            
            # Lemn și produse din lemn
            "timber", "unfinished", "furniture", "boat", "hull", "antique", "cabinet", "vintage", "dresser",
            "carved", "figurine", "musical", "instrument", "ornate", "frame", "ship", "reclaimed", "barn",
            "driftwood", "mask", "primitive", "tool", "handle", "toy",
            
            # Finisaje și acoperiri
            "cracked", "lacquer", "peeling", "bubbled", "chipped", "enamel", "flaking", "shellac", "polyurethane",
            "damaged", "spotted", "stain", "coating", "marks", "texture", "drip", "unpolished", "textured", "wall", 
            "imperfect", "application",
            
            # Obiecte de artă și antichități
            "restoration", "project", "museum", "artifact", "archaeological", "find", "historical", "relic", "family", 
            "heirloom", "vintage", "collectible", "classical", "pottery", "primitive", "artwork",
            "tombstone", "monument", "plaque", "marker", "inscription",
            
            # Concepte abstracte legate de imperfecțiune
            "draft", "unpolished", "manuscript", "raw", "creative", "work", "unrefined", "concept", "rough", "diamond",
            "hidden", "potential", "undeveloped", "talent", "unfinished", "masterpiece", "progress",
            "imperfect", "beauty", "natural", "state", "primitive", "form", "original", "condition", "untapped", "possibility"
        ],
        
        "Steam": [
            # Forme de gheață și fenomene de îngheț
            "ice", "freeze", "cold", "frost", "snow", "glacier", "chill", "hail", "permafrost", "iceberg",
            "frozen", "lake", "winter", "storm", "arctic", "tundra", "food", "sculpture", "pipe", "age",
            
            # Fenomene naturale de îngheț
            "polar", "cap", "waterfall", "crystal", "ground", "wonderland", "fishing",
            "river", "sheet", "ocean", "cube", "avalanche", "debris", "drift", "dam",
            "black", "rain", "sleet", "precipitation", "pellets", "blanket",
            
            # Efecte ale frigului asupra organismelor
            "frostbite", "hypothermia", "extremities", "stunned", "animal", "hibernating", "creature",
            "embryo", "preserved", "specimen", "animation", "tissue", "sample",
            "remains", "mammoth", "woolly", "rhinoceros", "mummy", "body",
            
            # Tehnologii și structuri de frig
            "cryogenic", "chamber", "industrial", "freezer", "storage", "facility", "refrigeration", "unit", "house",
            "burn", "product", "deep", "cooling", "system", "air", "conditioning", "heat", "exchanger",
            "thermal", "insulation", "chain", "logistics", "temperature", "controlled", "transport", "shipping", "container",
            
            # Metafore și concepte abstracte legate de frig
            "heart", "shoulder", "stare", "assets", "war", "queen", "moment",
            "reception", "storage", "time", "case", "account", "pack", "feet",
            "emotional", "creative", "block", "fear", "paralyzed", "terror", "suspended", "decision",
            
            # Fenomene cosmice și geologice de frig
            "exoplanet", "moon", "comet", "nucleus", "methane", "nitrogen", "deposit",
            "carbon", "dioxide", "interstellar", "cloud", "cosmic", "deep", "absolute", "zero", "environment",
            "planetary", "core", "earth", "period", "prehistoric", "shelf"
        ],
        
        "Acid": [
            # Materiale de bază vulnerabile
            "metal", "skin", "fabric", "human", "animal", "bone", "rubber", "food", "jewelry", "plastic",
            "limestone", "marble", "concrete", "tooth", "enamel", "coral", "reef", "pearl", "necklace", "chalk", "drawing",
            
            # Documente și artefacte culturale
            "scroll", "document", "photo", "dress", "garment", "carpet",
            "jacket", "shirt", "manuscript", "book", "collection", "museum", "archive",
            "record", "artifact", "evidence", "specimen",
            "discovery", "remain", "tool", "weapon", "art",
            
            
            # Metale și bijuterii
            "spoon", "ring", "watch", "wiring", "can",
            "necklace", "earring", "bracelet",
            "gemstone", "heirloom", "jewel", "crown", "scepter", "chalice",
            
            # Sisteme biologice și țesuturi
            "ecosystem", "species", "habitat", "organism", "structure",
            "material", "sample", "protein", "enzyme", "process",
            "pathway", "system", "nerve", "response", "tract", "tissue",
            "vessel", "gland", "organ", "development",
            
            # Unelte
            "hammer", "screwdriver", "wrench", "pliers", "drill", "saw", "chisel", "level", "tape", 
            "measure", "axe", "shovel", "rake", "hoe", "mallet", "vise", "file", "clamp", "sander", 
            "lathe", "anvil", "pickaxe", "crowbar", "trowel", "jackhammer", "toolbox", "socket", 
            "weld", "grinder", "stud", "finder"

            # Animale mici și prăzi
            "animal", "rabbit", "squirrel", "chipmunk", "marmot", "beaver", "otter", "raccoon",
            "porcupine", "skunk", "weasel", "marten", "fisher", "wolverine", "lynx", "bobcat",
            "bird", "turkey", "grouse", "pheasant", "quail", "duck", "goose",
            "salmon", "trout", "spawn", "frog", "toad", "salamander", "snake", "lizard",
        ],
        
        "Gust": [
            # Obiecte ușoare și materiale
            "tumbleweed", "dust", "leaves", "flame", "smoke", "ashes", "sand", "balloon", "kite", "feather",
            "airplane", "dandelion", "seed", "leaf"
            
            # Obiecte zburătoare și în mișcare
            "chime", "insect", "butterfly", "petal", "soil", "grass",
            "paraglider", "parachute", "bird",
            "eagle", "jellyfish", "ship",
            "sail", "flag", "banner", "ribbon", "awning",
        
        ],
        
        "Boulder": [
            # Materiale fragile și obiecte din sticlă
            "glass", "window", "fragile", "pottery", "phone", "screen", "laptop", "glasses", "computer", "bottle",
            "crystal", "vase", "china", "cabinet", "porcelain", "doll", "wine", "mirror", "chandelier", "bulb",
            
            # Obiecte din sticlă și cristal
            "table", "case", "greenhouse", "terrarium", "aquarium", "stained", "eyeglasses",
            "microscope", "telescope", "lens", "face", "instrument", "equipment",
            "clock", "decanter", "cut", "lead", "bohemian", "murano", "art",
            "venetian", "blown", "laboratory", "glassware", "tube", "array", "petri", "dish", "collection",
            
            # Dispozitive electronice și ecrane
            "smartphone", "display", "tablet", "television", "panel", "monitor", "watch",
            "headset", "reality", "reader", "console",
            "device", "camera", "recorder", "drone", "security",
            "medical", "imaging", "cockpit", "control", "billboard", "kiosk",
            
            # Obiecte de artă și colecții fragile
            "figurine", "thin", "eggshell", "fine", "ball", "globe",
            "sculpture", "fossil", "pottery", "fragment", "exhibit",
            "artifact", "relic", "treasure", "masterpiece", "item",
            "edition", "piece", "heirloom", "treasure",
            
            # Structuri și arhitectură din sticlă
            "door", "skylight", "ceiling", "wall", "bridge", "elevator",
            "staircase", "floor", "dome", "pyramid", "skyscraper", "house",
            "conservatory", "solarium", "atrium", "arcade", "building",
            "architecture", "structure", "design",
            
            
        ],
        
        "Drill": [
            # Materiale și suprafețe de bază
            "wood", "wall", "metal", "hole", "brick", "cement", "building", "drywall", "plastic", "floor",
            "concrete", "barrier", "stone", "sculpture", "marble", "countertop", "granite", "monument", "steel", "safe",
            
            # Structuri de securitate și bariere
            "door", "panel", "bunker", "structure", "vault",
            "cell", "vehicle", "glass", "hardened", "plate",
            "hull", "shell", "blast", "room", "gate",
            "reinforced", "shelter", "fortification", "defensive", "wall",
            
            # Materiale de construcție și suprafețe
            "hardwood", "floor", "ceramic", "tile", "wall", "sheet", "aluminum", "panel", "copper", "pipe",
            "bar", "beam", "bronze", "plate", "titanium", "frame", "carbon", "fiber", "composite", "material",
            "reinforced", "plastic", "laminate", "element", "bearing", "wall",
            "foundation", "pillar", "support", "column", "feature", "material",
            
            # Dispozitive electronice și ecrane
            "smartphone", "display", "tablet", "television", "panel", "monitor", "watch",
            "headset", "reality", "reader", "console",
            "device", "camera", "recorder", "drone", "security",
            "imaging", "cockpit", "control", "billboard", "kiosk",

        ],
        
        "Vacation": [
            # Stresori de muncă și presiuni
            "stress", "work", "burnout", "anxiety", "deadlines", "overwork", "pressure", "exhaustion", "fatigue", "routine",
            "corporate", "grind", "meetings", "email", "overload", "performance", "review", "quarterly", "report",
            
            # Activități și responsabilități profesionale
            "budget", "planning", "project", "deadline", "overtime", "hours", "workplace", "politics", "office", "drama",
            "customer", "complaint", "demanding", "boss", "difficult", "client", "emergency", "failure",
            "crisis", "supply", "chain", "issue", "market", "crash", "business", "travel", "commute",
            
            # Presiuni temporale și program încărcat
            "rush", "hour", "traffic", "packed", "subway", "lunch", "night", "morning", "weekend", "work",
            "holiday", "interruption", "canceled", "plans", "postponed", "celebration", "imbalance",
            "availability", "connected", "notification", "anxiety", "leash",
            
            # Stresori moderni și tehnologici
            "information", "overload", "digital", "burnout", "zoom", "fatigue", "screen", "time", "excess", "stress",
            "social", "media", "pressure", "comparison", "distraction", "addiction", "connectivity",
            "anxiety", "doomscrolling", "fear", "missing",
            
            # Presiuni sociale și relaționale
            "obligation", "expectation", "tension", "responsibility",
            "burden", "care", "stress", "difficulty", "proceeding",
            "worry", "pressure", "payment",
            
            # Concepte abstracte de epuizare și presiune
            "malaise", "dread", "crisis", "regret",
            "potential", "dream", "emptiness",
            "numbness", "fatigue", "exhaustion", "compassion", "decision", "fatigue",
            "analysis", "overload", "anxiety", "perfectionism",
        ],
        
        "Fire": [
            # Materiale combustibile de bază
            "book", "wood", "paper", "cloth", "forest", "building", "plastic", "house", "furniture", "curtains",
            "manuscript", "archive", "collection", "bridge", "cabin",
            
            # Structuri și construcții din lemn
            "timber", "frame", "bamboo", "hut", "straw", "roof", "cottage", "lantern", "creation",
            "document", "certificate", "license", "album", "church",
            "theater", "temple", "shrine", "center", "hall",
            "schoolhouse", "barn", "bridge", "outpost", "settlement",
            
            # Materiale textile și țesături
            "clothing", "tapestry", "drapes", "upholstery", "carpet",
            "fabric", "curtain", "blanket", "garment", "material",
            "clothing", "quilt", "rug", "tapestry", "afghan",
            "blanket", "garment", "suit", "dress", "creation",
            
            # Ecosisteme și medii naturale
            "park", "woodland", "forest", "grove", "habitat",
            "forest", "woodland", "rainforest", "swamp", "grove",
            "stand", "forest", "woodland", "grove", "forest",
            "grove", "swamp", "woodland", "stand", "canopy",
            
            # Obiecte de artă și artefacte culturale
            "furniture", "artifact", "toy", "painting",
            "artwork", "photograph", "book", "edition", "manuscript",
            "text", "codex", "scroll", "document", "page",
            "collection", "exhibition", "archive", "heritage", "legacy",
            
        ],
        
        "Drought": [
            # Vegetație și ecosisteme
            "plant", "crop", "river", "lake", "soil", "tree", "grass", "vegetation", "garden", "orchard",
            "rainforest", "wetland", "marsh", "swamp", "oasis", "valley", "land",
            
            # Terenuri agricole și culturi
            "farmland", "rice", "paddy", "wheat", "field", "corn", "crop", "vegetable", "garden", "flower", "bed",
            "botanical", "garden", "greenhouse", "hydroponics", "system", "irrigation", "network", "reservoir",
            "soybean", "plantation", "cotton", "field", "sugarcane", "plantation", "coffee", "farm", "tea", "garden",
            "vineyard", "grove", "orchard", "farm", "field", "garden",
            
            # Surse și sisteme de apă
            "spring", "aquifer", "table", "stream", "waterfall",
            "island", "ecosystem", "forest", "reef", "pond",
            "garden", "fountain", "garden", "farm", "delta",
            "watershed", "catchment", "basin", "floodplain",
            
            # Ecosisteme dependente de apă
            "ecosystem", "habitat", "bog", "moor", "land", "fen", "ecosystem",
            "pool", "pond", "stream", "river", "oasis",
            "forest", "ecosystem", "plant", "species",
            "organism", "wildlife", "chain", "biodiversity",
            
            # Comunități și infrastructuri dependente de apă
            "community", "society", "village", "settlement",
            "town", "community", "industry", "power",
            "facility", "district", "network", "system",
            "distribution", "supply", "spring",
            
            # Concepte abstracte de abundență și sustenabilitate
            "balance", "health", "service", "capital",
            "hotspot", "richness", "diversity", "potential",
            "resilience", "yield", "capacity", "system",
            "economy", "process", "resource", "abundance",
            "ecosystem", "community", "civilization", "future"
        ],
        
        "Water": [
            # Foc și fenomene asociate
            "fire", "blaze", "lava", "smoke", "ash", "flame", "ember", "wildfire", "dust", "desert",
            "fire", "building", "eruption", "rock", "flow",
            
            # Incendii și dezastre
            "oil", "fire", "chemical", "blaze", "explosion", "mine",
            "fire", "fire", "spacecraft", "launch", "impact",
            "manuscript", "arrow", "light", "effigy", "fire",
            
            # Fenomene de ardere și semnalizare
            "flare", "bridge", "earth", "ruin", "remains",
            "platform", "well", "shipwreck", "pyre", "fire",
            "conflagration", "inferno", "firestorm", "wave", "surge",
            "combustion", "point", "source", "material", "load",
            
            # Medii aride și deșertice
            "dune", "wasteland",
            "plain", "flat", "desert", "ground", "land",
            "disaster", "shortage"
            
            # Fenomene extreme de căldură
            "heat", "maximum", "temperature", "heatwave", "radiation",
            "exposure", "radiation", "emission", "signature", "image",
            "spike", "trend", "pollution",
            "effect", "trapping", "expansion",
            

        ],
        
        "Vacuum": [
            # Particule și resturi
            "air", "debris", "dust", "crumbs", "dirt", "particle", "sand", "spiderweb", "fiber", "clean",
            "pollen", "hair", "dandruff", "skin", "mite", "allergen", "spore",
            
            # Particule fine și pulberi
            "powder", "sawdust", "chip", "filing", "scrap", "lint",
            "fiber", "residue", "crumb", "crust", "piece",
            "kernel", "fragment", "rice", "sugar",
            
            # Resturi alimentare și organice
            "grounds", "leaves", "flakes", "powder", "dust",
            "soda", "crystal", "flake", "particle", "matter",
            "peel", "skin", "shell", "husk", "chaff",
            "fragment", "dust", "fiber", "scale", "shell",
            
            # Particule industriale și de mediu
            "dust", "debris", "particle", "fiber", "dust",
            "dust", "powder", "fragment", "dust", "fiber",
            "chip", "flake", "residue", "dust", "particle",
            "shaving", "fragment", "crumb", "shard", "dust",
            
        ],
        
        "Laser": [
            # Suprafețe reflectorizante și materiale
            "mirror", "plastic", "metal", "sensor", "lens", "fiber", "circuit", "glass", "panel", "robot",
            "surface", "steel", "chrome", "finish", "object", "plate",
            
            # Metale și suprafețe metalice
            "sheet", "foil", "ornament", "implant", "jewelry",
            "steel", "aluminum", "plating", "coating", "galvanization",
            "leaf", "foil", "wiring", "statue", "railing",
            "structure", "surface",
            
            # Echipamente optice și senzori
            "equipment", "sensor", "dish", "array", "tower",
            "system", "camera", "detector", "sensor", "meter",
            "detector", "sensor", "analyzer", "device",
            "scanner", "reader", "detector", "recognition", "identification",
            
            # Hard things to cut
            "metal", "steel", "iron", "diamond", "granite", "concrete", "brick",
            "stone", "marble", "ceramic", "bone", "ivory", "glass", "chain", "wire",
            "rebar", "armor", "slate", "tile", "obsidian", "shell", "crystal", 
            "carbide", "titanium", "alloy", "brickwork", "cement", "boulder", 
            "rock", "pebble"

        ],
        
        "Life Raft": [
            # Situații de înec și dezastre maritime
            "drowning", "ocean", "storm", "waves", "sea", "capsize", "shipwreck", "flood", "river", "sinking",
            "victim", "sailor", "castaway", "explorer", "crew",
            
            # Dezastre naturale și evacuări
            "survivor", "refugee", "victim", "evacuation",
            "accident", "disaster", "emergency", "catastrophe",
            "crisis", "tragedy", "distress", "canoe",
            "accident", "disaster", "emergency",
            
            # Inundații și creșterea nivelului apei
            "flooding", "submersion", "surge", "wave", "storm",
            
        ],
        
        "Bear Trap": [
            # Animale și prădători
            "leg", "foot", "animal", "hunter", "deer", "wolf", "bear", "hiker", "camper", "predator",
            "beast", "creature", "lion", "boar", "hog", "coyote",
            
            # Animale sălbatice și vânătoare
            "fox", "badger", "wolverine", "lynx", "bobcat", "raccoon", "opossum", "rabbit", "squirrel",
            "moose", "elk", "caribou", "bison", "antelope", "goat", "sheep", "horse",
            "herd", "cattle", "livestock", "animal", "specimen", "catch",
            "target", "quarry", "prey", "animal", "creature",
            
            # Oameni în sălbăticie
            "photographer", "researcher", "ranger", "visitor", "child",
            "party", "team", "dog", "guide", "poacher", "warden",
            "explorer", "enthusiast", "expert", "competitor",
            "runner", "biker", "skier", "snowshoer", "trekker",
            "adventurer", "leader", "guide", "instructor", "scientist",
            
            # Animale vulnerabile și specii protejate
            "species", "animal", "creature", "population", "wildlife",
            "target", "species", "individual", "animal", "specimen",
            "population", "subject", "census", "survey", "pattern",
            "range", "corridor"
            
            # Concepte abstracte de vulnerabilitate și capcană
            "victim", "target", "subject", "mark", "prey",
            "individual", "person", "entity", "position", "situation",
            "temptation", "lure", "opportunity", "promise", "danger",
            "threat", "peril", "hazard", "risk"
        ],
        
        "Diamond Cage": [
            # Infractori și fugitivi
            "thief", "intruder", "escape", "burglar", "prisoner", "robber", "enemy", "spy", "infiltrator", "fugitive",
            "criminal", "jewel", "thief", "art", "thief", "bank", "robber", "escapee", "fugitive",
            
            # Criminali periculoși și amenințări
            "convict", "killer", "terrorist", "leader", "boss", "don", "lord",
            "dealer", "trader", "counterfeiter", "hacker", "criminal", "thief",
            "spy", "saboteur", "agent", "agent", "operative",
            "assassin", "mercenary", "hunter", "soldier", "deserter", "criminal",
            
            # Prizonieri și deținuți
            "prisoner", "dissident", "revolutionary", "fighter", "insurrectionist",
            "enemy", "suspect", "hostage", "victim", "individual",
            "person", "subject", "captive", "prisoner", "convict",
            "inmate", "prisoner", "convict", "offender", "criminal",
            
            # Animale periculoase și creaturi
            "predator", "beast", "animal", "creature", "monster",
            "beast", "creature", "entity", "being", "horror",  "beast", "animal", "creature", "monster",
            "beast", "creature", "entity", "being", "horror",
            "organism", "specimen", "subject", "animal",
            "form", "visitor", "entity", "species", "organism",
        ],
        
        "Dam": [
            # Inundații și cursuri de apă
            "flood", "river", "overflow", "lake", "stream", "waterfall", "current", "watershed", "canal", "basin",
            "flash", "surge", "melt", "break", "breach", "failure",
            
            # Sisteme de apă și infrastructură
            "overflow", "failure", "system", "supply", "ecosystem",
            "migration", "run", "delta", "habitat", "community",
            "village", "settlement", "farm", "town", "port",
            "plant", "station", "system", "network",
            
            
            # Concepte abstracte de flux și barieră
            "flow", "current", "progression", "advance", "movement",
            "momentum", "force", "pressure", "accumulation", "tension",
            "burden", "weight", "volume", "level",
            "point", "threshold", "point", "release", "breach"
        ],
        
        "Mutation": [
            # Elemente genetice și biologice
            "gene", "dna", "organism", "virus", "bacteria", "cell", "chromosome", "species", "mutation", "evolution",
            "code", "sequence", "genome", "project", "trait", "disorder",
            
            # Condiții genetice și modificări
            "condition", "disease", "predisposition", "damage",
            "exposure", "contamination", "weapon", "virus",
            "specimen", "subject", "trial", "experiment", "attempt",
            "life", "organism", "crop", "animal",
            
            # Evoluție și adaptare
            "species", "organism", "species", "end",
            "selection", "adaptation", "pressure", "bottleneck",
            "drift", "effect", "population", "speciation", "evolution",
            "adaptation", "development", "race", "evolution",
            "equilibrium", "radiation", "niche", "adaptation",
            
            # Sisteme biologice și procese
            "system", "system", "function", "process", "respiration",
        ],
        
        "Kevlar Vest": [
            # Proiectile și arme
            "bullet", "knife", "stab", "attack", "shrapnel", "projectile", "gunfire", "assault", "weapon", "puncture",
            "round", "shot", "fire", "blast", "discharge",
            
            # Muniție și proiectile specializate
            "round", "bullet", "ammunition", "round",
            "bullet", "knife", "bayonet", "dagger", "switchblade",
            "stiletto", "knife", "shuriken", "tip", "bolt", "point",
            
            # Arme specializate și proiectile
            "dart", "penetrator", "round", "projectile", "round",
            "bullet", "round", "ammunition", "jacket", "bullet",
            "shot", "pellet", "bullet", "round", "dart",
            "round", "canister", "projectile", "grenade",
            
            # Atacuri și amenințări fizice
            "assault", "trauma", "impact", "blow", "strike",
            "attack", "force", "wound", "injury", "blow",
            "attempt", "hit", "execution", "killing", "hit",
            "attack", "shooting", "shooter", "assault", "extremist",
            
            # Concepte abstracte de protecție și vulnerabilitate
            "danger", "threat", "peril", "situation", "hazard",
            "risk", "vulnerability"
        ],
        
        "Jackhammer": [
            # Materiale dure și suprafețe
            "concrete", "rock", "pavement", "stone", "road", "wall", "floor", "building", "cement", "ground",
            "bunker", "shelter", "vault", "safe", "cell",
            
            # Structuri istorice și monumente
            "ruins", "site", "monument", "sculpture", "statue",
            "countertop", "roof", "street", "pathway", "bridge",
            "aqueduct", "castle", "fortress", "wall", "pyramid",
            "stonehenge", "statue", "rushmore", "monument", "arch",
            
            # Formațiuni geologice și structuri naturale
            "formation", "cave", "quarry", "mountain", "layer",
            "column", "arch", "cliff", "vein", "cave",
            "forest", "bed", "deposit", "mine", "seam",
            "mine", "mine", "pipe", "vein", "deposit",
            
            # Infrastructură urbană și construcții
            "street", "pavement", "support", "wall", "structure",
            "pillar", "wall", "wall", "breakwater", "jetty",
            "barrier", "wall", "perimeter", "fortification", "wall",
        
        ],
        
        "Signal Jammer": [
            # Comunicații și semnale
            "radio", "signal", "communication", "gps", "wifi", "cellphone", "satellite", "broadcast", "transmission", "call", "music",
            "broadcast", "signal", "call", "message", "coordination",
            
            # Comunicații militare și tactice
            "communication", "command", "operation", "mission",
            "control", "operation", "vehicle", "car", "system",
            "control", "navigation", "coordination", "management",
            "telemetry", "uplink", "communication", "network",
            
            # Sisteme de comunicații avansate
            "astronomy", "project", "signal", "communication",
            "entanglement", "interface", "link", "transmission",
            "network", "transfer", "uploading", "consciousness",
            "connection", "overlay", "integration", "projection",
            
            # Rețele și infrastructură de comunicații
            "network", "infrastructure", "grid", "backbone",
            "network", "transmission", "exchange", "communication",
            "protocol", "connection", "communication", "identification",
            "relay", "constellation", "system", "network",
            
            # Sisteme de alertă și siguranță
            "system", "network", "notification", "alert",
            "warning", "detection", "siren", "tracking",
            "alert", "broadcast", "announcement", "order",
            "alert", "detection", "monitoring", "network",
            
        ],
        
        "Grizzly": [
            # Oameni în sălbăticie
            "camper", "hiker", "hunter", "human", "deer", "moose", "sheep", "wolf", "fox", "tourist",
            "photographer", "biologist", "ranger", "guide", "watcher",
            
            # Activități în aer liber și recreere
            "forager", "picker", "survivalist", "climber", "runner",
            "skier", "snowshoer", "backpacker", "camper", "enthusiast",
            "enthusiast", "party", "troop", "class", "camp",
            
            # Animale mici și prăzi
            "animal", "rabbit", "squirrel", "chipmunk", "marmot", "beaver", "otter", "raccoon",
            "porcupine", "skunk", "weasel", "marten", "fisher", "wolverine", "lynx", "bobcat",
            "bird", "turkey", "grouse", "pheasant", "quail", "duck", "goose",
            "salmon", "trout", "spawn", "frog", "toad", "salamander", "snake", "lizard",
            
            # Animale domestice și animale de fermă
            "dog", "cat", "animal", "livestock", "herd", "cow",
            "steer", "flock", "producer", "herd", "goat", "goat",
            "stable", "pony", "mule", "animal", "coop", "layer",
            "bird", "farm", "pen", "producer", "hutch", "farm",
            
            # Concepte abstracte de vulnerabilitate și pradă
            "target", "individual", "creature", "being", "opponent",
            "adversary", "competitor"
        ],
        
        "Reinforced Steel Door": [
            # Intruși și amenințări
            "burglar", "thief", "breakin", "intruder", "enemy", "attacker", "spy", "force", "explosion", "zombie",
            "invader", "robber", "burglar", "thief", "crime",
            
            # Atacuri și asalturi
            "attack", "assault", "team", "raid", "agents",
            "ram", "charge", "entry", "lance", "torch",
            "drill", "spreader", "life", "sledgehammer", "hammer",
            
            # Amenințări apocaliptice și supranaturale
            "horde", "army", "crowd", "dead", "night", "dead",
            "outbreak", "spread", "vector", "zero", "threat",
            "invasion", "attack", "entity", "being", "creature",
            "presence", "spirit", "ghost", "specter", "activity",
            
            # Dezastre naturale și catastrofe
            "force",
            "front", "fire", "flood", "mudslide",
            "impact", "strike", "pulse", "leak",
            "fallout", "disaster",
        ],
        
        "Bulldozer": [
            # Structuri și construcții
            "building", "tree", "debris", "wall", "house", "car", "bridge", "fence", "rocks", "road",
            "temple", "site", "dig", "landmark", "building",
            
            # Medii naturale și ecosisteme
            "forest", "woodland", "habitat", "sanctuary", "reserve",
            "garden", "park", "playground", "field", "area",
            "ecosystem", "habitat", "environment", "formation", "forest",
            "reef", "pool", "meadow", "forest", "sanctuary",
            
            # Comunități și așezări umane
            "encampment", "settlement", "village", "dwelling", "site",
            "neighborhood", "enclave", "district", "community", "quarter",
            "town", "village", "community", "settlement", "town",
            "hamlet", "outpost", "community", "village", "town",
            
            # Mișcări de rezistență și proteste
            "protest", "activist", "effort", "movement", "defender",
            "resistance", "movement", "preservation", "protection", "conservation",
            "organizing", "movement", "activism", "protest", "demonstration",
            "disobedience", "resistance", "chain", "camp", "movement",
            
            # Buildings
            "house", "hut", "cottage", "mansion", "skyscraper", "tower", 
            "apartment", "condominium", "castle", "fortress", "barn", 
            "warehouse", "shed", "garage", "villa", "temple", "church",
            "cathedral", "mosque", "pagoda", "monastery", "palace",
            "lighthouse", "prison", "school", "hospital", "library",
            "station", "factory", "mill"
        ],
        
        "Sonic Boom": [
            # Obiecte fragile și structuri din sticlă
            "window", "glass", "structure", "building", "door", "roof", "wall", "panel", "ceiling", "chimney",
            "chandelier", "mirror", "window", "greenhouse", "conservatory",
            
            # Arhitectură și structuri din sticlă
            "skyscraper", "architecture", "bridge", "deck", "elevator",
            "dome", "roof", "skylight", "ceiling", "wall",
            "partition", "case", "exhibit", "installation", "showcase",
            "tank", "terrarium", "vivarium", "display", "enclosure",
            
            # Instrumente și echipamente sensibile
            "instrument", "equipment", "apparatus", "setup", "device",
            "sensor", "instrument", "equipment", "tool", "device",
            "system", "assembly", "mechanism", "mirror", "stage",
            "alignment", "interferometer", "spectrometer", "chromatograph", "microscope",
            
            # Obiecte de artă și colecții fragile
            "china", "collection", "figurine", "art", "sculpture",
            "artifact", "display", "find", "fossil", "pottery",
            "manuscript", "book", "text", "parchment", "document",
            "painting", "art", "drawing", "sketch", "rendering",
            
            # Sisteme biologice sensibile la sunet
            "animal", "colony", "pod", "migration", "sanctuary",
            "hearing", "system", "structure", "membrane", "bones",
            "fluid", "nerve", "mechanism", "system", "function",
            "ability", "navigation", "orientation", "hearing", "discrimination",
            
            # Concepte abstracte de armonie și echilibru
            "balance", "harmony", "equilibrium", "arrangement", "stability",
            "organization", "calibration", "tuning", "adjustment", "alignment",
            "coordination", "interaction", "relationship", "connection", "association",
            "distinction", "difference", "variation", "deviation", "margin"
        ],
        
        "Robot": [
            # Muncitori și profesii umane
            "human", "worker", "machine", "employee", "laborer", "operator", "driver", "soldier", "assistant", "engineer",
            "worker", "line", "staff", "job", "labor",
            
            # Locuri de muncă și ocupații
            "picker", "manager", "clerk", "driver", "operator",
            "driver", "operator", "conductor", "pilot", "captain",
            "worker", "cashier", "teller", "service", "receptionist",
            "guard", "watchman", "officer", "personnel", "unit",
            
            # Profesii periculoase și muncă fizică
            "worker", "miner", "worker", "lumberjack", "profession",
            "fisher", "cleaner", "climber", "worker", "worker",
            "firefighter", "responder", "relief", "rescue", "handler",
            "expert", "disposal", "squad", "team", "forces",
            
            # Servicii și îngrijire
            "aide", "provider", "worker", "teacher", "assistant",
            "therapist", "therapist", "specialist", "therapist", "trainer",
            "cleaner", "staff", "worker", "technician", "provider",
            "preparation", "chef", "staff", "server", "worker",
            
            # Concepte abstracte de muncă și efort uman
            "touch", "connection", "intelligence", "understanding", "response",
            "thinking", "expression", "solution", "idea", "approach",
            "judgment", "reasoning", "decision", "choice", "action",
            "sensitivity", "awareness", "context", "knowledge", "wisdom"
        ],
        
        "Love": [
            # Emoții negative și stări sufletești
            "hate", "anger", "loneliness", "sadness", "rage", "fear", "conflict", "pain", "depression", "isolation",
            "rivalry", "grudge", "feud", "enemy", "foe",
            
            # Ură și ostilitate
            "hatred", "resentment", "animosity", "contempt", "disdain",
            "rage", "fury", "temper", "anger", "hostility",
            "spite", "relationship", "interaction", "dynamic", "pattern",
            "treatment", "pleasure", "intent", "action", "behavior",
            
            # Frică și anxietate
            "fear", "anxiety", "dread", "terror", "panic",
            "worry", "nervousness", "apprehension", "doubt", "uncertainty",
            "phobia", "anxiety", "fear", "issue", "sensitivity",
            "response", "trigger", "episode", "attack", "disorder",
            
            # Conflict și violență
            "war", "conflict", "fighting", "violence", "suffering",
            "dispute", "argument", "competition", "rivalry", "contest",
            "confrontation", "abuse", "attack", "warfare", "combat",
            "division", "battle", "clash", "conflict", "tension",
            
            # Singurătate și izolare
            "loneliness", "rejection", "child", "elder", "confinement",
            "isolation", "emptiness", "solitude", "alienation", "disconnection",
            "exclusion", "ostracism", "estrangement", "abandonment", "termination",
            "isolation", "loneliness", "disconnect", "separation", "distance",
            
            # Concepte abstracte de negativitate și suferință
            "void", "darkness", "despair", "outlook", "worldview",
            "perspective", "attitude", "disappointment", "hope", "dream",
            "faith", "belief", "principle", "value", "ideal",
            "bankruptcy", "failure", "flaw", "breach", "collapse"
        ],
        
        "Therapy": [
            # Traume și probleme psihologice
            "trauma", "stress", "anxiety", "depression", "fear", "grief", "sadness", "guilt", "anger", "confusion",
            "stress", "fatigue", "shock", "neurosis", "guilt",
            
            # Experiențe traumatice și abuz
            "abuse", "violence", "assault", "crime", "attack",
            "disaster", "survivor", "trauma", "complication", "pain",
            "assault", "abuse", "manipulation", "control", "gaslighting",
            "abuse", "relationship", "dynamic", "behavior", "cycle",
            
            # Boli și suferință fizică
            "illness", "diagnosis", "disease", "decline", "loss",
            "condition", "disorder", "disease", "syndrome", "illness",
            "disability", "limitation", "impairment", "loss", "problem", "disorder", "difficulty",
            "issue", "syndrome", "condition", "disorder", "problem",
            
            # Pierdere și doliu
            "bereavement", "loss", "death", "aftermath", "accident",
            "aftermath", "relationship", "wound", "issues", "disorder",
            "grief", "mourning", "loss", "reaction", "separation",
            "loss", "death", "loss", "death", "suicide",
            
            # Probleme de sănătate mintală
            "illness", "condition", "disorder", "disturbance", "disorder",
            "disorder", "spectrum", "state", "disorder", "reaction",
            "pattern", "disorder", "dysmorphia", "behavior", "ideation",
            "dependence", "addiction", "addiction", "behavior", "control",
            
            # Probleme relaționale și sociale
            "conflict", "dysfunction", "challenge", "problem", "issue",
            "breakdown", "violation", "confusion", "imbalance", "dynamic",
            "anxiety", "pattern", "cycle", "sensitivity", "fear",
            "difficulty", "inability", "unavailability", "resistance", "avoidance",
            
            # Concepte abstracte de suferință și vindecare
            "wound", "scar", "crisis", "question", "confusion",
            "loss", "absence", "conflict", "injury", "dilemma",
            "critic", "spiral", "burden", "weight", "shadow",
            "judgment", "evaluation", "standard", "expectation", "ideal"
        ],
        
        "Disease": [
            # Sisteme biologice și sănătate
            "body", "organ", "immune", "virus", "bacteria", "infection", "fever", "sickness", "symptom", "illness", "freedom", "teamwork", "peace", "calm",
            "community", "population", "society", "civilization", "age",
            
            # Comunități sănătoase și relații
            "nation", "relationship", "effort", "project", "support",
            "health", "program", "care", "lifestyle", "nutrition",
            "fitness", "wellbeing", "stability", "health", "wellness",
            "vitality", "cohesion", "vibrancy", "expression", "flourishing",
            
            # Progres și inovație
            "breakthrough", "discovery", "advancement", "solution", "approach",
            "progress", "expansion", "growth", "development", "achievement",
            "innovation", "prosperity", "growth", "development", "progress",
            "evolution", "advancement", "renaissance", "explosion", "enlightenment",
            
            # Rezistență și adaptare
            "immunity", "constitution", "resistance", "response", "advantage",
            "system", "defense", "protection", "adaptation", "mutation",
            "mechanism", "feature", "trait", "benefit", "success",
            "resilience", "survival", "adaptation", "response", "adjustment",
            
            # Concepte abstracte de sănătate și armonie
            "ecosystem", "environment", "relationship", "cycle", "balance",
            "connection", "interaction", "system", "function", "effect",
            "integration", "whole", "system", "network", "web",
            "economy", "design", "model", "approach", "solution"

            # Humans
            "man", "woman", "child", "adult", "elderly", "teenager", "baby", "person", "individual", "human", "doctor", "teacher", "scientist", "engineer", "nurse", "chef", "farmer", "worker", "soldier", "athlete", "artist", "actor", "musician", "writer", "driver", "pilot", "lawyer", "student", "politician", "leader", "employer", "employee", "parent", "sibling", "friend", "stranger", "guest"

        ],

        "Confidence": [
            # Frică și îndoială
            "fear", "doubt", "insecurity", "anxiety", "hesitation", "shyness", "nervousness", "uncertainty", "timidity", "reluctance",
            "fright", "anxiety", "fear", "phobia", "agoraphobia",
            
            # Sindromul impostorului și auto-sabotaj
            "syndrome", "doubt", "talk", "voice", "sabotage",
            "paralysis", "paralysis", "overload", "phobia", "failure",
            "success", "judgment", "rejection", "abandonment", "inadequacy",
            "criticism", "judgment", "standard", "tendency", "expectation",
            
            # Traume și experiențe negative
            "trauma", "humiliation", "embarrassment", "criticism", "disapproval",
            "bullying", "rejection", "exclusion", "failure", "mistake",
            "setback", "disappointment", "criticism", "review", "feedback",
            "rejection", "failure", "anxiety", "fear", "avoidance",
            
            # Perfecționism și standarde înalte
            "perfectionism", "standards", "goals", "judgment", "attitude",
            "thinking", "perspective", "viewpoint", "mindset", "expectation",
            "preparation", "planning", "rehearsal", "practice", "preparation",
            "pressure", "stress", "demand", "requirement", "execution",
            
        ],
        
        "Absorption": [
            # Lichide și substanțe
            "water", "ink", "oil", "liquid", "gas", "light", "moisture", "sound", "heat", "nutrient",
            "water", "tide", "wave", "surge", "rainfall",
            
            # Scurgeri și deversări
            "spill", "leak", "waste", "effluent", "runoff",
            "material", "waste", "substance", "compound", "chemical",
            "product", "oil", "fuel", "spill", "leak",
            "solvent", "agent", "compound", "thinner", "solution",
            
            # Gaze și emisii
            "gas", "emission", "release", "smoke", "exhaust",
            "emission", "output", "smoke", "product", "residue",
            "gas", "emission", "seepage", "gas", "release",
            "pollutant", "toxin", "matter", "particle", "contaminant",
            
            # Energie și radiație
            "radiation", "ray", "heat", "energy", "frequency",
            "radiation", "ray", "beam", "stream", "flux",
            "radiation", "radiation", "wave", "spectrum", "pulse",
            "transfer", "radiation", "flow", "current", "energy",
            
        ],
        
        "Freeze": [
            # Apă și cursuri de apă
            "water", "river", "plant", "stream", "lake", "glacier", "pond", "ice", "snow", "hail",
            "waterfall", "rapids", "creek", "spring", "fountain",
            
            # Vegetație și creștere
            "rainforest", "vegetation", "garden", "meadow", "field",
            "crop", "fruit", "seed", "sapling", "flower",
            "leaf", "frond", "tendril", "vine", "root",
            "seed", "flower", "plant", "grass", "fern",
            
            # Procese biologice și mișcare
            "organism", "cell", "bacteria", "virus", "pathogen",
            "microbe", "protozoa", "amoeba", "plankton", "algae",
            "heart", "blood", "lung", "stomach", "kidney",
            "brain", "neuron", "synapse", "muscle", "joint",
            
            # Procese fizice și mișcare
            "reaction", "motion", "vibration", "fluctuation", "movement",
            "current", "impulse", "field", "pull", "decay",
            "fission", "reaction", "process", "action", "folding",
            "formation", "growth", "weathering", "process", "deposition",
            
            # Concepte abstracte de progres și mișcare
            "momentum", "process", "development", "system", "technology",
            "progress", "evolution", "movement", "change", "growth",
            "development", "process", "advancement", "progress", "expansion",
            "growth", "development", "journey", "evolution", "expansion"
        ],
        
        "Encryption": [
            # Date și comunicații
            "data", "message", "communication", "file", "password", "email", "information", "network", "internet", "transmission",
            "secret", "document", "file", "report", "information",
            
            # Informații sensibile guvernamentale și militare
            "intelligence", "data", "operation", "mission", "ops",
            "code", "data", "system", "network", "plan",
            "cable", "intelligence", "information", "security", "defense",
            "asset", "agent", "operative", "agent", "cell",
            
            # Secrete corporative și proprietate intelectuală
            "secret", "secret", "formula", "strategy", "advantage",
            "plan", "target", "research", "data", "strategy",
            "development", "breakthrough", "application", "property", "material",
            "code", "design", "specification", "process", "control",
            
            # Informații personale și date private
            "information", "correspondence", "confession", "disclosure", "diary",
            "record", "transaction", "data", "portfolio", "information",
            "record", "information", "profile", "data", "identifier",
            "history", "habit", "record", "connection", "status",
        ],
        
        "Proof": [
            # Teorii și afirmații nefondate
            "theory", "claim", "hypothesis", "statement", "argument", "evidence", "idea", "belief", "fact", "concept",
            "theory", "belief", "pseudoscience", "superstition", "legend",
            
            # Dezinformare și informații false
            "claim", "misinformation", "disinformation", "propaganda", "news",
            "report", "evidence", "hearsay", "rumor", "gossip",
            "story", "evidence", "photo", "video", "recording",
            "quote", "statistic", "data", "truth", "fact",
            
            # Retorică politică și manipulare
            "spin", "promise", "rhetoric", "statistic", "data",
            "claim", "statement", "reporting", "coverage", "account",
            "appeal", "mongering", "tactic", "message", "statement",
            "rhetoric", "sentiment", "view", "position", "opinion",
            
            # Erori logice și gândire defectuoasă  
            "sentiment", "view", "position", "opinion",
        ],
        
        "War": [
            # Pace și societate
            "peace", "city", "nation", "country", "army", "soldier", "civilization", "conflict", "battle", "population",
            "society", "community", "alliance", "solution", "settlement",
            
            # Patrimoniu cultural și realizări
            "heritage", "treasure", "wonder", "achievement", "advancement",
            "monument", "site", "treasure", "landmark", "heritage",
            "masterpiece", "classic", "composition", "tradition", "achievement",
            "breakthrough", "innovation", "discovery", "marvel", "triumph",
            
            # Populații civile și grupuri vulnerabile
            "population", "bystander", "group", "family", "person",
            "women", "children", "population", "individual", "patient", "institution",
            "facility", "worker", "organization", "force", "observer",
            "infrastructure", "utility", "supply", "source", "resource",
            
            # Dezvoltare și cultură
            "nation", "economy", "culture", "people", "minority",
            "diversity", "heritage", "tradition", "practice", "thought",
            "system", "institution", "facility", "repository", "resource",
            "community", "expression", "festival", "celebration", "ritual",
            
            # Concepte abstracte de pace și cooperare
            "stability", "order", "peace", "harmony", "brotherhood",
            "understanding", "dialogue", "cooperation", "respect", "coexistence",
            "humanity", "ground", "value", "principle", "foundation",
            "wisdom", "knowledge", "lesson", "experience", "insight"
        ],
        
        "Dynamite": [
            # Structuri și construcții
            "bridge", "wall", "mountain", "building", "house", "cave", "road", "tunnel", "dam", "rock",
            "monument", "landmark", "site", "heritage", "wonder",
            
            # Clădiri înalte și structuri urbane
            "skyscraper", "tower", "complex", "mall", "stadium",
            "building", "structure", "center", "complex", "venue",
            "block", "development", "renewal", "center", "area",
            "district", "hub", "quarter", "zone", "center",
            
            # Clădiri guvernamentale și instituții
            "building", "house", "palace", "court", "bank",
            "headquarters", "center", "mission", "compound", "building",
            "office", "hall", "courthouse", "station", "department",
            "base", "installation", "facility", "complex", "headquarters",
            
            # Infrastructură critică și facilități
            "complex", "campus", "facility", "laboratory", "center",
            "hub", "station", "terminal", "facility", "interchange",
            "plant", "grid", "treatment", "system", "management",
            "center", "center", "exchange", "facility", "uplink",

            # Fortresses
            "castle", "fortress", "keep", "stronghold", "bastion", "citadel", "fort", "watchtower", "wall", "moat", "gatehouse", "rampart", "turret", "bunker", "fortification", "outpost", "guardhouse", "tower", "palace", "castle wall", "barricade", "defense", "military base", "command center", "armory", "garrison", "military fortress", "redoubt", "sentry box"

        ],
        
        "Propaganda": [
            # Adevăr și informații obiective
            "truth", "information", "news", "media", "report", "opinion", "article", "broadcast", "story", "speech",
            "journalism", "reporting", "piece", "evidence", "source",
            
            # Știință și cercetare
            "consensus", "research", "study", "analysis", "knowledge",
            "evidence", "result", "data", "analysis", "measurement",
            "assessment", "study", "trial", "test", "finding",
            "rigor", "precision", "scrutiny", "verification", "confirmation",
            
            # Surse istorice și documentare
            "record", "document", "account", "testimony", "event",
            "artifact", "document", "material", "evidence", "finding",
            "record", "evidence", "layer", "sample", "data",
            "manuscript", "text", "inscription", "code", "hieroglyph",
            
            # Verificare și corectitudine
            "verification", "sources", "data", "statement", "fact",
            "organization", "process", "procedure", "method", "assessment",
            "correction", "notice", "oversight", "standard", "ethics",
            "disclosure", "declaration", "policy", "measure", "guideline",
            
            # Concepte abstracte de gândire critică
            "thinking", "analysis", "argument", "perspective", "understanding",
            "honesty", "fairness", "discipline", "evaluation", "assessment",
            "inquiry", "consideration", "judgment", "examination", "observation",
            "viewpoints", "perspectives", "interpretations", "explanations", "theories"
        ],
        
        "Evacuation": [
            # Crize și dezastre
            "crisis", "war", "infection", "zombie", "city", "fire", "earthquake", "attack", "building", "disaster",
            "meltdown", "leak", "spill", "gas", "hazard",
            
            # Dezastre naturale și fenomene extreme
            "eruption", "warning", "approach", "sighting", "surge",
            "spread", "fire", "risk", "threat", "danger",
            "storm", "condition", "storm", "event", "strike",
            "heat", "emergency", "storm", "sandstorm", "crisis",
            
            # Amenințări de securitate și atacuri
            "threat", "shooter", "situation", "threat", "unrest",
            "conflict", "invasion", "bombardment", "strike", "barrage",
            "warfare", "fighting", "action", "activity", "operation",
            "outbreak", "protest", "demonstration", "upheaval", "collapse",
            
            # Urgențe medicale și boli
            "outbreak", "pandemic", "pathogen", "infection", "emergency",
            "spread", "risk", "vector", "chain", "zero",
            "breach", "failure", "violation", "breakdown", "compromise",
            "overflow"
        ],
        
        "Persistence": [
            # Obstacole și provocări
            "chess", "sport", "passion",
            "obstacle", "challenge", "difficulty", "hardship", "setback", "failure", "defeat",
            "task", "barrier", "odds", "situation", "cause",
            
            # Renunțare și abandonare
            "giving", "surrender", "resignation", "abandonment", "withdrawal",
            "flag", "towel", "defeat", "loss", "failure",
            "decision", "down", "away", "out", "out",
            "quitting", "stopping", "losses", "on", "direction",
            
            # Atitudini negative și lipsă de motivație
            "laziness", "procrastination", "apathy", "indifference", "disinterest",
            "motivation", "drive", "ambition", "passion", "enthusiasm",
            "depletion", "exhaustion", "drain", "loss", "reduction",
            "avoidance", "aversion", "postponement", "extension", "delay",
        ],
        
        "Reforestation": [
            # Terenuri degradate și deșertice
            "desert", "barren", "field", "plain", "hillside", "meadow", "savanna", "land", "valley", "steppe",
            "wasteland", "bowl", "dune", "outcrop", "slope",
            
            # Zone defrișate și exploatate
            "area", "forest", "woodland", "jungle", "timber",
            "clearing", "harvest", "extraction", "production",
            "plantation", "source", "collection", "production", "gathering",
            "conversion", "expansion", "development", "creation", "land",
            
            # Situri industriale și zone poluate
            "pit", "zone", "platform",
            "land", "soil", "dump", "waste", "runoff",
            "factory", "mine", "quarry", "well", "plant",
            "ruin", "wasteland", "remnant", "aftermath",
            
            # Concepte abstracte de degradare și epuizare
            "farmland", "pasture", "field", "soil", "ruin",
            "collapse", "loss", "extinction", "destruction", "degradation",
            "damage", "depletion", "practice", "footprint", "emission",
            "impact", "warming", "process", "erosion", "scarcity"
        ],
        
        "H-bomb": [
            # Așezări umane și civilizație
            "city", "nation", "world", "continent", "civilization", "country", "population", "state", "town", "region",
            "area", "center", "city", "district", "hub",
            
            # Patrimoniu cultural și istoric
            "landmark", "monument", "wonder", "heritage", "find",
            "collection", "archive", "institution", "center", "facility",
            "building", "monument", "center", "institution", "venue",
            "record", "manuscript", "document", "source", "artifact",
            
            # Ecosisteme și mediu
            "ecosystem", "environment", "habitat", "reserve", "species",
            "hotspot", "community", "web", "flow", "cycle",
            "species", "organism", "population", "flora", "fauna",
            "system", "network", "reserve", "resource", "ecosystem",
            
            # Sisteme agricole și alimentare
            "land", "community", "production", "cultivation", "raising",
            "system", "soil", "field", "storage", "distribution",
            "bank", "repository", "diversity", "variety", "breed",
            "practice", "farming", "agriculture", "sovereignty", "security",
            
            # Concepte abstracte de viitor și umanitate
            "generation", "child", "youth", "elder", "population",
            "potential", "possibility", "capacity", "promise", "talent",
            "evolution", "development", "progress", "advancement", "improvement",
            "coexistence", "living", "future", "prosperity", "wellbeing"
        ],
        
        "AI Kill Switch": [
            # Sisteme AI și automatizări
            "robot", "ai", "machine", "automation", "drone", "system", "android", "bot", "software", "emergency",
            "intelligence", "system", "machine", "computer", "robot",
            
            # Sisteme militare autonome
            "weapon", "drone", "robot", "machine", "automaton",
            "vehicle", "weapon", "missile", "bomb", "munition",
            "defense", "security", "patrol", "drone", "system",
            "network", "system", "management", "coordination", "logistics",
            
            # Sisteme de supraveghere și control
            "network", "system", "algorithm", "recognition", "prediction",
            "surveillance", "monitoring", "tracking", "analysis", "recognition",
            "policing", "prevention", "assessment", "evaluation", "profiling",
            "collection", "gathering", "invasion", "monitoring", "surveillance",
            
            # Sisteme financiare și economice
            "algorithm", "bot", "manipulation", "control", "concentration",
            "trading", "crash", "volatility", "fluctuation", "instability",
            "banking", "lending", "scoring", "calculation", "determination",
            "allocation", "distribution", "planning", "forecasting", "prediction",
            
            # Concepte abstracte de control și autonomie
            "algorithm", "filter", "control", "manipulation", "guidance",
            "bubble", "chamber", "silo", "isolation", "limitation",
            "economy", "optimization", "maximization", "exploitation", "conditioning",
            "erosion", "reduction", "limitation", "narrowing", "diminishment"
        ],
        
        "Nanobot Swarm": [
            # Sisteme biologice și celule
            "virus", "cell", "bacteria", "organism", "tissue", "body", "infection", "pathogen", "plague", "disease",
            "system", "cell", "response", "defense", "barrier",
            
            # Organe și țesuturi vitale
            "organ", "tissue", "brain", "muscle", "capacity",
            "filtration", "tract", "system", "gland", "vessel",
            "marrow", "production", "cell", "cell", "regeneration",
            "repair", "healing", "formation", "response", "reaction",
            
            # Desperate
            "hopeless", "despair", "anxiety", "panic", "urgency", "distress", "helpless", "crisis", "desperation", "emergency", "uncontrollable", "frenzied", "frantic", "overwhelmed", "tormented", "unstable", "dismay", "suffocating", "loss", "broken", "alone", "abandoned", "fear", "wretched", "endangered", "cornered", "trapped", "unhinged"

        ]
    }


    # 3. Calculam vectorii medii pentru fiecare unealta
    categories_vectors = {}
    for tool, keywords in tools_categories.items():
        vec = average_vector(keywords, embeddings)
        if vec is not None:
            categories_vectors[tool] = vec
        else:
            print(f"Atentie: Nu s-a putut crea vector pentru categoria {tool}.")

    # 4. Cerem cuvinte sau expresii de la utilizator pana cand se introduce '0'
    while True:
        word_or_phrase = input("\nIntroduceti un cuvant sau expresie pentru a-l clasifica, sau '0' pentru a iesi: ")

        if word_or_phrase == '0':
            print("Programul s-a inchis.")
            break

        classify_tool(word_or_phrase, embeddings, categories_vectors)
