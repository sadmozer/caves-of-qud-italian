from pathlib import Path
from lxml import etree
import re
import sys

EN_DIR = Path("../ExampleLanguage")
IT_DIR = Path("../ItalianLanguage/languages/lang-it")

placeholder_pattern = re.compile(r"\{\d+\}|%[sd]")

errors = []
warnings = []


def load_xml(path):
    try:
        parser = etree.XMLParser(recover=False)
        tree = etree.parse(str(path), parser)
        return tree
    except Exception as e:
        errors.append(f"Malformed XML: {path} -> {e}")
        return None


def extract_text_nodes(elem):
    texts = []

    if elem.text and elem.text.strip():
        texts.append(elem.text.strip())

    for child in elem:
        texts.extend(extract_text_nodes(child))

    if elem.tail and elem.tail.strip():
        texts.append(elem.tail.strip())

    return texts


def check_placeholders(en_text, it_text, file):
    en_p = sorted(placeholder_pattern.findall(en_text))
    it_p = sorted(placeholder_pattern.findall(it_text))

    if en_p != it_p:
        errors.append(
            f"[Line {en_elem.sourceline}] "
            f"Placeholder mismatch in {file}\\n"
            f"EN: {en_text}\\n"
            f"IT: {it_text}"
        )


def compare_elements(en_elem, it_elem, file):

    if en_elem.tag != it_elem.tag:
        errors.append(
            f"[Line {en_elem.sourceline}] "
            f"Tag mismatch in {file}: "
            f"{en_elem.tag} != {it_elem.tag}"
        )

    if sorted(en_elem.attrib.keys()) != sorted(it_elem.attrib.keys()):
        errors.append(
            f"[Line {en_elem.sourceline}] "
            f"Attribute mismatch in {file}: "
            f"{en_elem.tag}"
        )

    if en_elem.text and it_elem.text:
        check_placeholders(
            en_elem.text,
            it_elem.text,
            file
        )

        en_len = len(en_elem.text.strip())
        it_len = len(it_elem.text.strip())
        en_text = (en_elem.text or "").strip()
        it_text = (it_elem.text or "").strip()

        if en_len > 0:
            growth = ((it_len-en_len)/en_len)*100
            if growth > 50:
                warnings.append(
                    f"[Line {en_elem.sourceline}] "
                    f"Long translation (+{growth:.0f}%) "
                    f"in {file}: {it_text[:60]}"
                )


        if (
            en_text
            and it_text
            and en_text == it_text
        ):
            warnings.append(
                f"[Line {en_elem.sourceline}] "
                f"Possibly untranslated string in {file}: "
            )

    en_children = list(en_elem)
    it_children = list(it_elem)

    if len(en_children) != len(it_children):
        errors.append(
            f"[Line {en_elem.sourceline}] "
            f"Node count mismatch in {file}: {len(en_children)} != {len(it_children)}"
            f"{en_text[:60]}"
        )
        return

    for ec, ic in zip(en_children, it_children):
        compare_elements(ec, ic, file)


print(f"Scanning English directory: {EN_DIR.resolve()}")
print(f"Scanning Italian directory: {IT_DIR.resolve()}")

files = list(EN_DIR.rglob('*.xml'))
print(f"Found {len(files)} English XML files")

for en_file in files:

    print(f"Checking: {en_file}")

    rel = en_file.relative_to(EN_DIR)
    translated_name = en_file.name.replace(".example.xml", ".it.xml")

    it_file = en_file.parent.relative_to(EN_DIR)
    it_file = IT_DIR / it_file / translated_name


    if not it_file.exists():
        errors.append(f"Missing translated file: {rel}")
        continue

    en_tree = load_xml(en_file)
    it_tree = load_xml(it_file)

    if not en_tree or not it_tree:
        continue

    compare_elements(
        en_tree.getroot(),
        it_tree.getroot(),
        rel
    )

if warnings:
    print("\nWARNINGS:")
    for w in warnings:
        print(w)

if errors:
    print("\nERRORS:")
    for e in errors:
        print(e)
    sys.exit(1)

print("DEBUG SUMMARY")
print(f"Files checked: {len(list(EN_DIR.rglob('*.xml')))}")
print(f"Warnings: {len(warnings)}")
print(f"Errors: {len(errors)}")

print("All validations passed.")