import json
import re
import random 
import string 

# --- Configuration & Mappings (Populated based on our discussions) ---

DEFAULT_ITEM_IMG = "icons/svg/item-bag.svg"
DEFAULT_ACTOR_IMG = "icons/svg/mystery-man.svg"

TALENT_ACTIVATION_MAP = {
    "Passive": {"value": "Passive", "label": "SWFFG.TalentActivationsPassive"},
    "Active (Incidental)": {"value": "Active (Incidental)", "label": "SWFFG.TalentActivationsActiveIncidental"},
    "Active (Incidental, Out of Turn)": {"value": "Active (Incidental, Out of Turn)", "label": "SWFFG.TalentActivationsActiveIncidentalOutofTurn"},
    "Active (Action)": {"value": "Active (Action)", "label": "SWFFG.TalentActivationsActiveAction"},
    "Active (Maneuver)": {"value": "Active (Maneuver)", "label": "SWFFG.TalentActivationsActiveManeuver"},
}

SKILL_THEME_DATA = {}
ITEM_QUALITIES_DEFINITIONS = {}

QUALITY_NAME_TO_FFGIMPORTID_MAP = {
    "Accurate": "ACCURATE", "Auto-fire": "AUTOFIRE", "Blast": "BLAST", "Breach": "BREACH",
    "Burn": "BURN", "Concussive": "CONCUSSIVE", "Cumbersome": "CUMBERSOME",
    "Defensive": "DEFENSIVE", "Deflection": "DEFLECTION", "Disorient": "DISORIENT",
    "Ensnare": "ENSNARE", "Guided": "GUIDED", "Inferior": "INFERIOR",
    "Inaccurate": "INACCURATE", "Knockdown": "KNOCKDOWN", "Limited Ammo": "LIMITEDAMMO",
    "Linked": "LINKED", "Pierce": "PIERCE", "Prepare": "PREPARE",
    "Reinforced": "REINFORCED", "Slow-Firing": "SLOWFIRING", "Stun": "STUN",
    "Stun Damage": "STUNDAMAGE", "Sunder": "SUNDER", "Superior": "SUPERIOR",
    "Unwieldy": "UNWIELDY", "Vicious": "VICIOUS",
}

# --- Helper Functions ---

def generate_foundry_id(length=16):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_attribute_key():
    return 'attr_' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

def format_description(desc_array_or_string):
    if isinstance(desc_array_or_string, list):
        if not desc_array_or_string: return ""
        return "".join([f"<p>{p.strip()}</p>" for p in desc_array_or_string if p and p.strip()])
    elif isinstance(desc_array_or_string, str):
        if not desc_array_or_string.strip(): return ""
        # If it already looks like HTML (starts with <p>), return as is.
        if desc_array_or_string.strip().lower().startswith("<p>"):
            return desc_array_or_string.strip()
        return f"<p>{desc_array_or_string.strip()}</p>"
    return ""

def parse_name_and_rank_from_string(entry_string, default_rank=1):
    name = entry_string.strip()
    rank = default_rank
    is_ranked_explicitly = False
    match_rank_at_end = re.match(r"^(.*?)\s+(\d+)$", name)
    if match_rank_at_end:
        name = match_rank_at_end.group(1).strip()
        try:
            rank = int(match_rank_at_end.group(2))
            is_ranked_explicitly = True
        except ValueError: rank = default_rank
    else:
        match_paren_suffix = re.match(r"^(.*?)\s*\(.*\)$", name)
        if match_paren_suffix:
            name = match_paren_suffix.group(1).strip()
    return name, rank, is_ranked_explicitly


def get_skill_key_and_data(gr_skill_name, gr_skill_characteristic, gr_skill_category):
    normalized_gr_name_for_match = gr_skill_name.lower()
    if "(" in normalized_gr_name_for_match:
        normalized_gr_name_for_match = re.sub(r'\s*\((.*?)\)', r'-\1', normalized_gr_name_for_match).replace(" ", "")

    best_match_key = None
    for theme_key, theme_skill_def in SKILL_THEME_DATA.get("skills", {}).items():
        if theme_key.lower() == gr_skill_name.lower():
            best_match_key = theme_key; break
        if theme_key.lower() == normalized_gr_name_for_match:
            best_match_key = theme_key; break
        if "knowledge" in gr_skill_name.lower() and theme_key.lower() == "knowledge":
             best_match_key = theme_key; break

    if best_match_key and best_match_key in SKILL_THEME_DATA["skills"]:
        theme_skill = SKILL_THEME_DATA["skills"][best_match_key]
        abrev = theme_skill.get("abrev", "")
        if abrev.startswith("SWFFG.SkillsName"): 
            key_parts = [word[0] for word in re.findall(r'[A-Z][a-z]*', best_match_key.replace("-",""))]
            abrev = "".join(key_parts)[:3].upper() if key_parts else best_match_key[:3].upper()
        return {
            "key": best_match_key, "label": gr_skill_name,
            "characteristic": theme_skill.get("characteristic", gr_skill_characteristic.capitalize() if gr_skill_characteristic else "Brawn"),
            "type": theme_skill.get("type", gr_skill_category if gr_skill_category else "General"),
            "abrev": abrev, "groupskill": theme_skill.get("groupskill", False),
            "careerskill": theme_skill.get("careerskill", False), "max": theme_skill.get("max", 6),
            "custom": False
        }
    else: 
        key = gr_skill_name
        if "(" in key: key = re.sub(r'\s*\((.*?)\)\s*', r' \1 ', key)
        key = re.sub(r'[^a-zA-Z0-9\s]', '', key)
        key = "".join([word.capitalize() for word in key.split()])
        if not key: key = "CustomSkill" + generate_foundry_id(4)
        abrev_parts = [char for char in key if char.isupper()]
        abrev = "".join(abrev_parts)[:3] if abrev_parts else key[:3].upper()
        if not abrev: abrev = "CST"
        return {
            "key": key, "label": gr_skill_name,
            "characteristic": gr_skill_characteristic.capitalize() if gr_skill_characteristic else "Brawn",
            "type": gr_skill_category if gr_skill_category else "General",
            "abrev": abrev, "groupskill": False, "careerskill": False, "max": 6, "custom": True
        }

def create_item_modifier(gr_quality, item_type):
    ffg_import_id = QUALITY_NAME_TO_FFGIMPORTID_MAP.get(gr_quality["name"])
    modifier_definition = None

    if ffg_import_id and ffg_import_id in ITEM_QUALITIES_DEFINITIONS:
        modifier_definition = ITEM_QUALITIES_DEFINITIONS[ffg_import_id]
    else: 
        for key, mod_def in ITEM_QUALITIES_DEFINITIONS.items():
            if mod_def.get("flags", {}).get("starwarsffg", {}).get("ffgimportid", "").lower() == gr_quality["name"].lower().replace("-",""):
                modifier_definition = mod_def
                ffg_import_id = mod_def["flags"]["starwarsffg"]["ffgimportid"]
                break
            if mod_def.get("name", "").lower().startswith(gr_quality["name"].lower()):
                modifier_definition = mod_def
                ffg_import_id = mod_def.get("flags", {}).get("starwarsffg", {}).get("ffgimportid")
                break
    
    gr_rank = 1
    if gr_quality["name"] == "Reinforced":
        gr_rank = 0 
        if modifier_definition and "rank" in modifier_definition.get("system",{}):
             gr_rank = modifier_definition["system"]["rank"]
    elif "ranks" in gr_quality:
        try: gr_rank = int(gr_quality["ranks"])
        except (ValueError, TypeError): gr_rank = 1

    embedded_mod = {
        "_id": generate_foundry_id(),
        "name": modifier_definition.get("name") if modifier_definition else gr_quality["name"],
        "type": "itemmodifier",
        "img": modifier_definition.get("img") if modifier_definition else DEFAULT_ITEM_IMG,
        "effects": [],
        "system": {
            "description": modifier_definition.get("system", {}).get("description") if modifier_definition else format_description(gr_quality.get("description", [gr_quality["name"]])),
            "attributes": modifier_definition.get("system", {}).get("attributes", {}) if modifier_definition else {},
            "metadata": {"tags": ["itemmodifier", item_type], "sources": []}, 
            "type": modifier_definition.get("system", {}).get("type", item_type) if modifier_definition else item_type,
            "rank": gr_rank, "active": True
        }, "flags": {}
    }
    if ffg_import_id and modifier_definition:
         embedded_mod["flags"]["starwarsffg"] = {"ffgimportid": ffg_import_id }
    elif modifier_definition and "flags" in modifier_definition and "starwarsffg" in modifier_definition["flags"]:
         embedded_mod["flags"]["starwarsffg"] = {"ffgimportid": modifier_definition["flags"]["starwarsffg"].get("ffgimportid")}
    return embedded_mod

# --- Main Conversion Functions ---

def convert_adversaries(gr_data, gr_metadata_source):
    fvtt_actors = []
    for adv in gr_data.get("adversary", []):
        actor_items = []

        fvtt_skills = {}
        for skill in adv.get("skills", []):
            skill_data = get_skill_key_and_data(
                skill["name"], skill.get("characteristic"), skill.get("category")
            )
            fvtt_skills[skill_data["key"]] = {
                "label": skill_data["label"], "rank": int(skill.get("ranks", 0)),
                "characteristic": skill_data["characteristic"], "groupskill": skill_data["groupskill"],
                "careerskill": skill_data["careerskill"], "type": skill_data["type"],
                "max": skill_data["max"], "abrev": skill_data["abrev"], "custom": skill_data["custom"],
            }
        
        # Convert Talents (Embedded) - Now handles strings like "Adversary 2"
        for talent_entry in adv.get("talents", []):
            final_talent_name = "Unnamed Talent"
            final_talent_description_html = ""
            talent_rank = 1
            talent_is_ranked = False 
            activation_str = "Passive" 
            tier = 1 

            if isinstance(talent_entry, str):
                parsed_name, parsed_rank, rank_was_explicit = parse_name_and_rank_from_string(talent_entry)
                final_talent_name = parsed_name
                talent_rank = parsed_rank
                if rank_was_explicit or talent_rank > 1 : 
                    talent_is_ranked = True
                final_talent_description_html = format_description(f"See rules for {final_talent_name}.")
            elif isinstance(talent_entry, dict):
                talent_name_from_gr = talent_entry.get("name", "Unnamed Talent")
                talent_description_list = talent_entry.get("description")
                final_talent_name = talent_name_from_gr
                if not talent_description_list and len(talent_name_from_gr) > 60: 
                    final_talent_description_html = format_description(talent_name_from_gr)
                    name_match = re.match(r"([^()]+)(\s*\(.*\))?", talent_name_from_gr)
                    if name_match and name_match.group(1).strip(): final_talent_name = name_match.group(1).strip()
                elif talent_description_list: final_talent_description_html = format_description(talent_description_list)
                else: final_talent_description_html = format_description(f"See rules for {final_talent_name}.")
                if len(final_talent_name) > 60 and final_talent_name == talent_name_from_gr:
                    final_talent_name = " ".join(final_talent_name.split()[:5]) + "..."
                activation_str = talent_entry.get("activation", "Passive")
                talent_rank = int(talent_entry.get("ranks", 1))
                talent_is_ranked = talent_entry.get("ranked", False) or talent_rank > 1
                tier = int(talent_entry.get("tier", 1))
            else:
                print(f"Warning: Skipped unexpected talent format for {adv['name']}: {talent_entry}")
                continue 
            
            activation_data = TALENT_ACTIVATION_MAP.get(activation_str, {"value": activation_str, "label": activation_str})
            actor_items.append({
                "_id": generate_foundry_id(), "name": final_talent_name, "type": "talent",
                "img": DEFAULT_ITEM_IMG, "effects": [],
                "system": {
                    "description": final_talent_description_html, "attributes": {},
                    "metadata": {"tags": ["talent"], "sources": [{"name": gr_metadata_source["full"], "page": str(adv.get("page","N/A"))}]},
                    "activation": activation_data,
                    "ranks": {"ranked": talent_is_ranked, "current": talent_rank, "min": 0},
                    "isForceTalent": False, "isConflictTalent": False, "tier": tier, "trees": [],
                }})

        # Convert Abilities (Embedded) - Now handles dicts like {'name': 'Natural', ...}
        for ability_entry in adv.get("abilities", []): 
            ability_name = "Special Ability"; ability_description_html = ""
            page_num_for_source = str(adv.get("page","N/A")) 

            if isinstance(ability_entry, str):
                ability_description_html = format_description(ability_entry)
                match_name_paren = re.match(r"([^()]+)(\s*\(.*\))?:?", ability_entry)
                if match_name_paren and match_name_paren.group(1).strip():
                    potential_name = match_name_paren.group(1).strip()
                    if len(potential_name) <= 50: ability_name = potential_name
                    else:
                        ability_name = " ".join(ability_entry.split()[:5])
                        if len(ability_name) > 50 : ability_name = ability_name[:47] + "..."
                elif ability_entry.strip():
                    ability_name = " ".join(ability_entry.split()[:5])
                    if len(ability_name) > 50 : ability_name = ability_name[:47] + "..."
                if len(ability_name) < 5 and ability_name.lower() != "silhouette 0" and ability_name.lower() != "flyer":
                    ability_name = "Special Ability"
            elif isinstance(ability_entry, dict): 
                ability_name = ability_entry.get("name", "Special Ability")
                desc_from_dict = ability_entry.get("description", [f"See rules for {ability_name}."])
                ability_description_html = format_description(desc_from_dict) 
                page_num_for_source = str(ability_entry.get("page", adv.get("page", "N/A")))
            else: 
                print(f"Warning: Skipped unexpected ability format for {adv['name']}: {ability_entry}")
                continue
            
            actor_items.append({
                "_id": generate_foundry_id(), "name": ability_name, "type": "talent", 
                "img": DEFAULT_ITEM_IMG, "effects": [],
                "system": {
                    "description": ability_description_html, "attributes": {},
                    "metadata": {"tags": ["ability"], "sources": [{"name": gr_metadata_source["full"], "page": page_num_for_source}]},
                    "activation": {"value": "Passive", "label": "SWFFG.TalentActivationsPassive"},
                    "ranks": {"ranked": False, "current": 1, "min": 0}, "tier": 0, 
                }})
        
        for weapon in adv.get("weapons", []): 
            embedded_weapon_attributes = {}; base_damage_val = 0; char_for_skill_damage_mod = ""
            gr_damage_str = str(weapon.get("damage", "0"))
            gr_skill_name = weapon.get("skill", {}).get("name", "Melee")
            skill_char_for_damage = "Brawn" 
            if any(s_type in gr_skill_name.lower() for s_type in ["ranged", "gunnery"]): skill_char_for_damage = "Agility"
            if gr_damage_str.startswith("+") and skill_char_for_damage == "Brawn":
                base_damage_val = 0
                try:
                    damage_bonus = int(gr_damage_str[1:])
                    embedded_weapon_attributes[generate_attribute_key()] = {"modtype": "Weapon Stat", "value": damage_bonus, "mod": "damage"}
                    char_for_skill_damage_mod = "Brawn"
                except ValueError: pass 
            else:
                try: base_damage_val = int(gr_damage_str)
                except ValueError: base_damage_val = 0
            embedded_weapon_itemmodifiers = [create_item_modifier(q, "weapon") for q in weapon.get("qualities", [])]
            actor_items.append({
                "_id": generate_foundry_id(), "name": weapon["name"], "type": "weapon", "img": DEFAULT_ITEM_IMG, "effects": [],
                "system": {
                    "description": format_description(weapon.get("description", [f"A {weapon['name']}."])),
                    "attributes": embedded_weapon_attributes,
                    "metadata": {"tags": ["weapon"], "sources": [{"name": gr_metadata_source["full"], "page": str(adv.get("page","N/A"))}]},
                    "quantity": {"value": 1}, "encumbrance": {"value": int(weapon.get("encumbrance", 0))},
                    "price": {"value": int(weapon.get("price", 0))}, "rarity": {"value": int(weapon.get("rarity", 0))},
                    "hardpoints": {"value": 0}, "equippable": {"value": True, "equipped": True},
                    "itemattachment": [], "itemmodifier": embedded_weapon_itemmodifiers,
                    "skill": {"value": gr_skill_name}, 
                    "damage": {"value": base_damage_val}, "crit": {"value": int(weapon.get("critical", 0))},
                    "range": {"value": weapon.get("range", "Engaged")}, "special": {"value": ""},
                    "characteristic": {"value": char_for_skill_damage_mod}
                }})

        for gear_entry in adv.get("gear", []):
            item_type_fvtt = "gear"; item_name = "Unnamed Gear"; item_description_html = ""
            item_soak = 0; item_defense = 0; item_encumbrance = 0; item_price = 0; item_rarity = 0
            if isinstance(gear_entry, str):
                item_name = gear_entry 
                item_description_html = format_description(gear_entry)
                if "armor" in gear_entry.lower() or "soak" in gear_entry.lower() or "defense" in gear_entry.lower():
                    item_type_fvtt = "armour"
                    soak_match = re.search(r'(\+?\d+)\s*soak', gear_entry, re.IGNORECASE)
                    if soak_match:
                        try: item_soak = int(soak_match.group(1).replace("+",""))
                        except ValueError: pass 
                    defense_match = re.search(r'(\+?\d+)\s*defense', gear_entry, re.IGNORECASE)
                    if defense_match:
                        try: item_defense = int(defense_match.group(1).replace("+",""))
                        except ValueError: pass
                if len(item_name) > 50 :
                    name_candidate_match = re.match(r"([^()]+)(\s*\(.*\))?", item_name)
                    if name_candidate_match and name_candidate_match.group(1).strip(): item_name = name_candidate_match.group(1).strip()
                    else: item_name = " ".join(item_name.split()[:5]) + ("..." if len(item_name.split()) > 5 else "")
                if len(item_name) < 3: item_name = "Gear Item" if item_type_fvtt == "gear" else "Armor Piece"
            elif isinstance(gear_entry, dict): 
                item_name = gear_entry.get("name", "Unnamed Gear")
                item_description_html = format_description(gear_entry.get("description", [item_name]))
                item_encumbrance = int(gear_entry.get("encumbrance", 0))
                item_price = int(gear_entry.get("price", 0))
                item_rarity = int(gear_entry.get("rarity", 0))
                gr_item_type = gear_entry.get("type", "gear")
                if "soak" in gear_entry or "defense" in gear_entry or gr_item_type == "armor":
                    item_type_fvtt = "armour"; item_soak = int(gear_entry.get("soak", 0)); item_defense = int(gear_entry.get("defense", 0))
                else: item_type_fvtt = "gear" 
            else:
                print(f"Warning: Skipped unexpected gear format for {adv['name']}: {gear_entry}")
                continue
            embedded_item_system = {
                "description": item_description_html, "attributes": {},
                "metadata": {"tags": [item_type_fvtt], "sources": [{"name": gr_metadata_source["full"], "page": str(adv.get("page","N/A"))}]},
                "quantity": {"value": 1}, "encumbrance": {"value": item_encumbrance},
                "price": {"value": item_price}, "rarity": {"value": item_rarity},
                "equippable": {"value": True, "equipped": True}
            }
            if item_type_fvtt == "armour":
                embedded_item_system["soak"] = {"value": item_soak}; embedded_item_system["defence"] = {"value": item_defense}
                embedded_item_system["hardpoints"] = {"value": 0}
            actor_items.append({"_id": generate_foundry_id(), "name": item_name, "type": item_type_fvtt,
                                "img": DEFAULT_ITEM_IMG, "effects": [], "system": embedded_item_system})

        actor_id = generate_foundry_id()
        actor_type_fvtt = adv.get("type","rival").lower()
        gr_defense = adv.get("derived", {}).get("defense", [0,0])
        melee_defense, ranged_defense = 0, 0
        if isinstance(gr_defense, list) and len(gr_defense) >= 1:
            melee_defense = int(gr_defense[0])
            ranged_defense = int(gr_defense[1]) if len(gr_defense) > 1 else melee_defense
        elif isinstance(gr_defense, (int, float)): 
            melee_defense = int(gr_defense); ranged_defense = int(gr_defense)

        fvtt_actors.append({
            "_id": actor_id, "name": adv["name"], "type": actor_type_fvtt, "img": DEFAULT_ACTOR_IMG,
            "system": {
                "biography": format_description(adv.get("description", [])),
                "stats": {"wounds": {"max": int(adv.get("derived", {}).get("wounds", 10)), "value": int(adv.get("derived", {}).get("wounds", 10)), "min": 0},
                           "strain": {"max": int(adv.get("characteristics",{}).get("willpower",1)*2 if adv.get("characteristics",{}).get("willpower") else 10), 
                                      "value": int(adv.get("characteristics",{}).get("willpower",1)*2 if adv.get("characteristics",{}).get("willpower") else 10), "min": 0},
                           "soak": {"value": int(adv.get("derived", {}).get("soak", 0))},},
                "characteristics": {
                    "BRAWN": {"value": int(adv.get("characteristics",{}).get("brawn", 1)), "label": "Brawn"},
                    "AGILITY": {"value": int(adv.get("characteristics",{}).get("agility", 1)), "label": "Agility"},
                    "INTELLECT": {"value": int(adv.get("characteristics",{}).get("intellect", 1)), "label": "Intellect"},
                    "CUNNING": {"value": int(adv.get("characteristics",{}).get("cunning", 1)), "label": "Cunning"},
                    "WILLPOWER": {"value": int(adv.get("characteristics",{}).get("willpower", 1)), "label": "Willpower"},
                    "PRESENCE": {"value": int(adv.get("characteristics",{}).get("presence", 1)), "label": "Presence"},},
                "skills": fvtt_skills, "defence": {"melee": melee_defense, "ranged": ranged_defense},
                "quantity": {"value": 1, "max": 1, "type": "Number", "label": "Quantity"},
                "source": f"{gr_metadata_source['full']} pg. {adv.get('page', 'N/A')}",},
            "items": actor_items, "effects": [], "folder": None,
            "prototypeToken": {
                "name": adv["name"], "displayName": 20, "actorLink": False, "appendNumber": False, "prependAdjective": False,
                "texture": {"src": DEFAULT_ACTOR_IMG, "scaleX":1, "scaleY":1, "offsetX":0, "offsetY":0, "rotation":0, "tint":None},
                "width": 1, "height": 1, "lockRotation": False, "rotation": 0, "alpha": 1,
                "disposition": -1 if actor_type_fvtt in ["rival", "nemesis", "minion"] else 0,
                "displayBars": 20, "bar1": {"attribute": "stats.wounds"}, "bar2": {"attribute": "stats.strain"},
                "light": {"alpha": 0.5, "angle": 360, "bright": 0, "coloration": 1, "dim": 0, "attenuation": 0.5, "luminosity": 0.5, "saturation":0, "contrast":0, "shadows":0, "animation": {"type":None, "speed":5, "intensity":5, "reverse":False}, "darkness": {"min":0, "max":1}},
                "sight": {"enabled": False, "range": 0, "angle": 360, "visionMode": "basic", "color": None, "attenuation": 0.1, "brightness":0, "saturation":0, "contrast":0},
                "detectionModes": [],
            }, "flags": {"starwarsffg": {"config": {"enableAutoSoakCalculation": False, "enableCriticalInjuries": False}}}
        })
        if actor_type_fvtt == "minion":
            minion_wounds_per_minion = int(adv.get("derived", {}).get("wounds", 4))
            fvtt_actors[-1]["system"]["stats"]["wounds"]["max"] = minion_wounds_per_minion 
            fvtt_actors[-1]["system"]["stats"]["wounds"]["value"] = minion_wounds_per_minion
            fvtt_actors[-1]["system"]["quantity"]["value"] = 3 
            fvtt_actors[-1]["system"]["quantity"]["max"] = 5 
    return fvtt_actors

def convert_weapons(gr_data, gr_metadata_source):
    fvtt_weapons = []
    for item in gr_data.get("gear", []):
        if item.get("type") != "weapon": continue
        fvtt_attributes = {}; base_damage_val = 0; char_for_skill_damage_mod = "";
        gr_damage_str = str(item.get("damage", "0"))
        gr_skill_obj = item.get("skill", {}); gr_skill_name = gr_skill_obj.get("name", "Melee")
        gr_skill_char = "Brawn" 
        normalized_gr_skill_name_for_match = gr_skill_name.lower().replace(" (", "-").replace(")", "").replace(" ", "-")
        skill_theme_entry_key = None
        for theme_key in SKILL_THEME_DATA.get("skills", {}).keys():
            if theme_key.lower() == gr_skill_name.lower() or theme_key.lower() == normalized_gr_skill_name_for_match:
                skill_theme_entry_key = theme_key; break
        if skill_theme_entry_key and SKILL_THEME_DATA["skills"][skill_theme_entry_key].get("characteristic"):
            gr_skill_char = SKILL_THEME_DATA["skills"][skill_theme_entry_key]["characteristic"]
        
        if gr_damage_str.startswith("+") and gr_skill_char.lower() == "brawn":
            base_damage_val = 0
            try:
                damage_bonus = int(gr_damage_str[1:])
                fvtt_attributes[generate_attribute_key()] = {"modtype": "Weapon Stat", "value": damage_bonus, "mod": "damage"}
                char_for_skill_damage_mod = "Brawn"
            except ValueError: print(f"Warning: Could not parse damage bonus for {item['name']}: {gr_damage_str}")
        else:
            try: base_damage_val = int(gr_damage_str)
            except ValueError: base_damage_val = 0
        item_modifiers = [create_item_modifier(q, "weapon") for q in item.get("qualities", [])]
        fvtt_weapons.append({
            "_id": generate_foundry_id(), "name": item["name"], "type": "weapon", "img": DEFAULT_ITEM_IMG,
            "system": {
                "description": format_description(item.get("description", [])), "attributes": fvtt_attributes,
                "metadata": {"tags": ["weapon"] + [s.get("name") for s in item.get("settings", []) if s.get("name")],
                             "sources": [{"name": gr_metadata_source['full'], "page": str(item.get('page', 'N/A'))}]},
                "quantity": {"value": 1, "type": "Number", "label": "Quantity", "abrev": "Qty"},
                "encumbrance": {"value": int(item.get("encumbrance", 0)), "type": "Number", "label": "Encumbrance", "abrev": "Encum"},
                "price": {"value": int(item.get("price", 0)), "type": "Number", "label": "Price"},
                "rarity": {"value": int(item.get("rarity", 0)), "type": "Number", "label": "Rarity"},
                "hardpoints": {"value": int(item.get("hardpoints", 0)), "type": "Number", "label": "Hard Points", "abrev": "HP"},
                "equippable": {"value": True, "type": "Boolean", "equipped": False},
                "itemattachment": [], "itemmodifier": item_modifiers,
                "skill": {"value": gr_skill_name, "type": "String", "label": "Skill"},
                "damage": {"value": base_damage_val, "type": "Number", "label": "Damage", "abrev": "Dam"},
                "crit": {"value": int(item.get("critical", 0)), "type": "Number", "label": "Critical Rating", "abrev": "Crit"},
                "range": {"value": item.get("range", "Engaged"), "type": "String", "label": "Range"},
                "special": {"value": "", "type": "String", "label": "Special"}, 
                "characteristic": {"value": char_for_skill_damage_mod}
            }, "effects": [], "folder": None, "flags": {}
        })
    return fvtt_weapons

def convert_armor(gr_data, gr_metadata_source):
    fvtt_armors = []
    for item in gr_data.get("gear", []):
        if item.get("type") != "armor": continue
        item_modifiers = [create_item_modifier(q, "armour") for q in item.get("qualities", [])]
        fvtt_armors.append({
            "_id": generate_foundry_id(), "name": item["name"], "type": "armour", "img": DEFAULT_ITEM_IMG,
            "system": {
                "description": format_description(item.get("description", [])), "attributes": {},
                "metadata": {"tags": ["armour"] + [s.get("name") for s in item.get("settings", []) if s.get("name")],
                             "sources": [{"name": gr_metadata_source['full'], "page": str(item.get('page', 'N/A'))}]},
                "quantity": {"value": 1, "type": "Number", "label": "Quantity", "abrev": "Qty"},
                "encumbrance": {"value": int(item.get("encumbrance", 0)), "type": "Number", "label": "Encumbrance", "abrev": "Encum"},
                "price": {"value": int(item.get("price", 0)), "type": "Number", "label": "Price"},
                "rarity": {"value": int(item.get("rarity", 0)), "type": "Number", "label": "Rarity"},
                "hardpoints": {"value": int(item.get("hardpoints", 0)), "type": "Number", "label": "Hard Points", "abrev": "HP"},
                "equippable": {"value": True, "type": "Boolean", "equipped": False},
                "itemattachment": [], "itemmodifier": item_modifiers,
                "defence": {"value": int(item.get("defense", 0)), "type": "Number", "label": "Defence", "abrev": "Def"},
                "soak": {"value": int(item.get("soak", 0)), "type": "Number", "label": "Soak"},
            }, "effects": [], "folder": None, "flags": {}
        })
    return fvtt_armors

def convert_talents(gr_data, gr_metadata_source):
    fvtt_talents = []
    for talent in gr_data.get("talent", []):
        activation_key = talent.get("activation", "Passive")
        activation_data = TALENT_ACTIVATION_MAP.get(activation_key, {"value": activation_key, "label": activation_key})
        fvtt_talents.append({
            "_id": generate_foundry_id(), "name": talent["name"], "type": "talent", "img": DEFAULT_ITEM_IMG,
            "system": {
                "description": format_description(talent.get("description", [])), "attributes": {},
                "metadata": {"tags": ["talent"] + [s.get("name") for s in talent.get("settings", []) if s.get("name")],
                             "sources": [{"name": gr_metadata_source['full'], "page": str(talent.get('page', 'N/A'))}]},
                "activation": activation_data,
                "ranks": {"ranked": talent.get("ranked", False), "current": 1, "min": 0 },
                "isForceTalent": False, "isConflictTalent": False,
                "tier": int(talent.get("tier", 1)), "trees": [], "longDesc": ""
            }, "effects": [], "folder": None, "flags": {}
        })
    return fvtt_talents

def convert_gear(gr_data, gr_metadata_source):
    fvtt_gear_items = []
    allowed_gear_types = ["gear", "implement", "cybernetic", "consumable", "medical"]
    for item in gr_data.get("gear", []):
        gr_item_type = item.get("type")
        if gr_item_type not in allowed_gear_types: continue
        fvtt_attributes = {} 
        if "Medkit" in item["name"] and "grants □ to Medicine checks" in "".join(item.get("description",[])):
             fvtt_attributes[generate_attribute_key()] = {"modtype": "Skill Boost", "mod": "Medicine", "value": 1, "label": "Medicine Boost (Medkit)"}
        item_modifiers = [create_item_modifier(q, "gear") for q in item.get("qualities", [])]
        fvtt_gear_items.append({
            "_id": generate_foundry_id(), "name": item["name"], "type": "gear", "img": DEFAULT_ITEM_IMG,
            "system": {
                "description": format_description(item.get("description", [])), "attributes": fvtt_attributes,
                "metadata": {"tags": ["gear", gr_item_type] + [s.get("name") for s in item.get("settings", []) if s.get("name")],
                             "sources": [{"name": gr_metadata_source['full'], "page": str(item.get('page', 'N/A'))}]},
                "quantity": {"value": 1, "type": "Number", "label": "Quantity", "abrev": "Qty"},
                "encumbrance": {"value": int(item.get("encumbrance", 0)), "type": "Number", "label": "Encumbrance", "abrev": "Encum"},
                "price": {"value": int(item.get("price", 0)), "type": "Number", "label": "Price"},
                "rarity": {"value": int(item.get("rarity", 0)), "type": "Number", "label": "Rarity"},
                "equippable": {"value": True, "type": "Boolean", "equipped": False},
                "itemattachment": [], "itemmodifier": item_modifiers, 
            }, "effects": [], "folder": None, "flags": {}
        })
    return fvtt_gear_items

def write_compendium_file(filename_prefix, pack_label, pack_type, items_data, system_id="starwarsffg"):
    output_path = f"{filename_prefix}_compendium_output.json" 
    package_name_part = filename_prefix.replace("_", "-") 
    compendium_data = {
        "package": f"world.{package_name_part}", 
        "metadata": {
            "name": package_name_part, "label": pack_label, "path": f"packs/{package_name_part}", 
            "type": pack_type, "system": system_id,
            "ownership": {"PLAYER": "OBSERVER", "ASSISTANT": "OWNER"}, "flags": {},
            "packageType": "world", "packageName": "genesys-custom-conversion", 
            "id": f"world.{package_name_part}"
        },
        "type": pack_type, "items": items_data, "folders": [], 
        "source": { "world": "your-world-name", "system": system_id, "version": {"core": "12.331", "system": "1.906"}}
    }
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(compendium_data, f, indent=2)
    print(f"Successfully wrote {pack_type} compendium to {output_path}")

def main():
    gr_filepath = "core-rule-book.json" 
    skill_theme_filepath = "swffg-skilltheme-genesys.json"
    item_qualities_filepath = "fvtt-Item-pack-starwarsffg-item-qualities.json"

    try:
        with open(gr_filepath, 'r', encoding='utf-8') as f: gr_data = json.load(f)
    except FileNotFoundError: print(f"Error: GenesysRef file not found at {gr_filepath}"); return
    except json.JSONDecodeError: print(f"Error: Could not decode JSON from {gr_filepath}"); return
    gr_metadata_source = gr_data.get("_meta", {}).get("source", {"full": "Genesys Core Rulebook", "abbreviation": "CRB"})

    global SKILL_THEME_DATA
    try:
        with open(skill_theme_filepath, 'r', encoding='utf-8') as f: SKILL_THEME_DATA = json.load(f)
    except FileNotFoundError: print(f"Warning: Skill theme file ({skill_theme_filepath}) not found.")
    except json.JSONDecodeError: print(f"Warning: Could not decode JSON from skill theme file.")

    global ITEM_QUALITIES_DEFINITIONS
    try:
        with open(item_qualities_filepath, 'r', encoding='utf-8') as f:
            qualities_pack_data = json.load(f)
            for item_quality in qualities_pack_data.get("items", []):
                ffg_id = item_quality.get("flags", {}).get("starwarsffg", {}).get("ffgimportid")
                key_to_use = ffg_id if ffg_id else item_quality.get("name", generate_foundry_id())
                ITEM_QUALITIES_DEFINITIONS[key_to_use] = item_quality
    except FileNotFoundError: print(f"Warning: Item qualities file ({item_qualities_filepath}) not found.")
    except json.JSONDecodeError: print(f"Warning: Could not decode JSON from item qualities file.")

    print("Starting conversion...")
    foundry_actors = convert_adversaries(gr_data, gr_metadata_source)
    foundry_weapons = convert_weapons(gr_data, gr_metadata_source)
    foundry_armor = convert_armor(gr_data, gr_metadata_source)
    foundry_talents = convert_talents(gr_data, gr_metadata_source)
    foundry_gear = convert_gear(gr_data, gr_metadata_source)
    print("Conversion functions finished.")

    if foundry_actors: write_compendium_file("genesys_actors", "Genesys Adversaries CRB", "Actor", foundry_actors)
    if foundry_weapons: write_compendium_file("genesys_weapons", "Genesys Weapons CRB", "Item", foundry_weapons)
    if foundry_armor: write_compendium_file("genesys_armor", "Genesys Armor CRB", "Item", foundry_armor)
    if foundry_talents: write_compendium_file("genesys_talents", "Genesys Talents CRB", "Item", foundry_talents)
    if foundry_gear: write_compendium_file("genesys_gear", "Genesys Gear CRB", "Item", foundry_gear)
    
    print("\nScript finished. Output files are .json files that mimic compendium pack structure.")

if __name__ == "__main__":
    main()