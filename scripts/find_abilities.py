import xml.etree.ElementTree as ET

def normalize(text):
    if text is None:
        return ""
    return text.replace("▶", "").strip()

# --- LOAD FILES ---
skills_tree = ET.parse("../ItalianLanguage/languages/Skills.it.xml")
skills_root = skills_tree.getroot()

strings_tree = ET.parse("../ItalianLanguage/languages/Strings.it.xml")
strings_root = strings_tree.getroot()

# --- BUILD CONTEXT MAP ---
context_map = {}

for s in strings_root.findall("string"):
    context = s.attrib.get("Context", "")
    text_it = normalize(s.text)

    if context:
        context_map.setdefault(context, []).append(text_it)

# --- MATCH ---
mismatches = []

for skill in skills_root.findall("skill"):
    skill_name = skill.attrib.get("Name", "")

    # 1. controlla la skill stessa
    display = normalize(skill.attrib.get("DisplayName", ""))
    snippet = normalize(skill.attrib.get("Snippet", ""))

    matching_contexts = [
        ctx for ctx in context_map
        if ctx.startswith(skill_name + " ")
    ]

    possible_translations = []
    for ctx in matching_contexts:
        possible_translations.extend(context_map[ctx])

    if possible_translations:
        if display and display not in possible_translations:
            mismatches.append((skill_name, "Skill DisplayName", display, possible_translations))
        if snippet and snippet not in possible_translations:
            mismatches.append((skill_name, "Skill Snippet", snippet, possible_translations))

    # 2. controlla i power dentro la skill
    for power in skill.findall("power"):
        power_name = power.attrib.get("Name", "")

        display = normalize(power.attrib.get("DisplayName", ""))
        snippet = normalize(power.attrib.get("Snippet", ""))

        matching_contexts = [
            ctx for ctx in context_map
            if ctx.startswith(power_name + " ")
        ]

        possible_translations = []
        for ctx in matching_contexts:
            possible_translations.extend(context_map[ctx])

        if not possible_translations:
            continue

        if display and display not in possible_translations:
            mismatches.append((power_name, "Power DisplayName", display, possible_translations))

        if snippet and snippet not in possible_translations:
            mismatches.append((power_name, "Power Snippet", snippet, possible_translations))

# --- OUTPUT ---
print("=== MISMATCH TROVATI ===\n")

for name, field, current, expected in mismatches:
    print(f"{name}")
    print(f"  Campo: {field}")
    print(f"  Attuale: {current}")
    print(f"  Possibili: {expected}")
    print("-" * 50)

print(f"\nTotale mismatch: {len(mismatches)}")