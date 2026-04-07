#!/usr/bin/env python3
"""
Caves of Qud — Strumenti di localizzazione italiana (unified)

Uso:
  python coq_traduzioni.py traduce  INPUT.xml OUTPUT.xml
      Prima passata: aggiunge ▶ a tutte le stringhe e applica le traduzioni note.

  python coq_traduzioni.py patch    INPUT.xml OUTPUT.xml
      Patch selettivo: aggiorna solo le voci presenti nel dizionario (con
      matching normalizzato per gestire \n vs &#10;).

  python coq_traduzioni.py estrai   INPUT.xml [OUTPUT.txt] [--stats]
      Estrae le stringhe ancora non tradotte (valore == ID).
"""
import sys
import re
import xml.etree.ElementTree as ET

from dizionario import TRADUZIONI


# ════════════════════════════════════════════════════════════════════════════
# FUNZIONI HELPER
# ════════════════════════════════════════════════════════════════════════════

def normalize(s):
    """Normalizza spazi e newline per il confronto (&#10; → \n → spazio)."""
    return re.sub(r'\s+', ' ', s.replace('\r\n', '\n').replace('\r', '\n')).strip()


# Regex per i token =commandKey:Xxx= / =commandKeyShort:Xxx= / =commandKeyConsole:Xxx=
_CMD_TOKEN_RE = re.compile(r'=commandKey(?:Short|Console)?:[^=]+=')

def _to_template(s):
    """Riduce ogni =commandKey*:Xxx= al placeholder generico =commandKey=."""
    return _CMD_TOKEN_RE.sub('=commandKey=', s)


# Tre mappe costruite una volta sola:
#   _NORM_MAP     — chiavi normalizzate (spazi/newline collassati)
#   _TMPL_MAP     — chiavi template (commandKey normalizzati) → valore originale
_NORM_MAP: dict = {}
_TMPL_MAP: dict = {}

def _get_norm_map():
    global _NORM_MAP
    if not _NORM_MAP:
        _NORM_MAP = {normalize(k): v for k, v in TRADUZIONI.items()}
    return _NORM_MAP

def _get_tmpl_map():
    global _TMPL_MAP
    if not _TMPL_MAP:
        for k, v in TRADUZIONI.items():
            tk = normalize(_to_template(k))
            if tk not in _TMPL_MAP:
                _TMPL_MAP[tk] = v
    return _TMPL_MAP


def _strip_tokens(s):
    """Rimuove tutti i token procedurali e di markup, lascia solo testo leggibile."""
    c = re.sub(r'=\w[^=]*=', '', s)                      # =token=
    c = re.sub(r'\{\{[^}]+\|([^}]+)\}\}', r'\1', c)      # {{color|text}} → text
    c = re.sub(r'\{\{[^}]+\}\}', '', c)                   # {{tag}}
    c = re.sub(r'[^a-zA-Z\s]', '', c)
    return c.strip()


def is_procedural(sid):
    """
    True solo se la stringa NON contiene abbastanza testo leggibile da tradurre.
    Una stringa come "Press =commandKey:X=" ha solo "Press" → < 10 char → procedural.
    Una stringa come "Look at the screen.\n\nPress =commandKey:X=" ha molto testo → NON procedural.
    """
    return len(_strip_tokens(sid)) < 10


def is_untranslated(sid, value):
    """True se il valore (senza ▶) è identico all'ID dopo normalizzazione."""
    if not value:
        return False
    return normalize(value.lstrip("▶")) == normalize(sid)


def _lookup(sid):
    """
    Cerca la traduzione con tre livelli di fallback:
      1. Match diretto su TRADUZIONI
      2. Match normalizzato (gestisce &#10; / \\n / spazi multipli)
      3. Match template: =commandKey:Xxx= → =commandKey= (copre kbm E gamepad
         con una sola voce nel dizionario)
    """
    # 1. Diretto
    if sid in TRADUZIONI:
        return TRADUZIONI[sid]
    # 2. Normalizzato
    norm_sid = normalize(sid)
    v = _get_norm_map().get(norm_sid)
    if v is not None:
        return v
    # 3. Template (solo se la stringa contiene almeno un token commandKey)
    if _CMD_TOKEN_RE.search(sid):
        tmpl_sid = normalize(_to_template(sid))
        v = _get_tmpl_map().get(tmpl_sid)
        if v is not None:
            # Reinserisce i token originali al posto dei placeholder =commandKey=
            tokens = _CMD_TOKEN_RE.findall(sid)
            result = v
            for tok in tokens:
                result = re.sub(r'=commandKey=', tok, result, count=1)
            return result
    return None


def get_translated_value(string_id, original_value):
    """Restituisce la traduzione con ▶ prefisso, o il valore originale marcato."""
    t = _lookup(string_id)
    if t is not None:
        return "▶" + t
    if original_value and original_value.startswith("▶"):
        return original_value
    if original_value:
        return "▶" + original_value
    return "▶" + string_id


def _write_elem(s, new_value):
    if s.get('Value') is not None:
        s.set('Value', new_value)
        s.text = None
    else:
        s.text = new_value


# ════════════════════════════════════════════════════════════════════════════
# MODALITÀ: traduce
# Prima passata: applica TRADUZIONI a tutti, marca tutti con ▶
# ════════════════════════════════════════════════════════════════════════════
def cmd_traduce(input_path, output_path):
    print(f"Lettura: {input_path}")
    tree = ET.parse(input_path)
    root = tree.getroot()
    strings = root.findall('string')
    total = len(strings)
    print(f"Stringhe trovate: {total}")
    tradotte = non_tradotte = 0
    for s in strings:
        sid = s.get('ID', '')
        orig = (s.get('Value') or s.text or '').strip()
        new_value = get_translated_value(sid, orig)
        if _lookup(sid) is not None:
            tradotte += 1
        else:
            non_tradotte += 1
        _write_elem(s, new_value)
    print(f"Tradotte: {tradotte} | Originale mantenuto: {non_tradotte} | Totale: {total}")
    tree.write(output_path, encoding='utf-8', xml_declaration=True)
    check = ET.parse(output_path).getroot().findall('string')
    print(f"Verifica output: {len(check)} stringhe — {'OK' if len(check) == total else 'ERRORE!'}")


# ════════════════════════════════════════════════════════════════════════════
# MODALITÀ: patch
# Aggiorna solo le voci presenti nel dizionario (match diretto + normalizzato).
# ════════════════════════════════════════════════════════════════════════════
def cmd_patch(input_path, output_path):
    print(f"Lettura: {input_path}")
    tree = ET.parse(input_path)
    root = tree.getroot()
    strings = root.findall('string')
    total = len(strings)
    patched = 0
    for s in strings:
        t = _lookup(s.get('ID', ''))
        if t is not None:
            _write_elem(s, "▶" + t)
            patched += 1
    print(f"Voci patchate: {patched} | Totale stringhe: {total}")
    tree.write(output_path, encoding='utf-8', xml_declaration=True)
    check = ET.parse(output_path).getroot().findall('string')
    print(f"Verifica output: {len(check)} stringhe — {'OK' if len(check) == total else 'ERRORE!'}")


# ════════════════════════════════════════════════════════════════════════════
# MODALITÀ: estrai
# Estrae le stringhe ancora non tradotte (valore == ID), esclude le procedurali.
# ════════════════════════════════════════════════════════════════════════════
def cmd_estrai(input_path, output_path=None, stats_only=False):
    print(f"Lettura: {input_path}", file=sys.stderr)
    root = ET.parse(input_path).getroot()
    strings = root.findall('string')
    total = len(strings)
    untranslated, proc_skip, translated = [], 0, 0

    for s in strings:
        sid = s.get('ID', '')
        val = (s.get('Value') or s.text or '').strip()
        if not is_untranslated(sid, val):
            translated += 1
            continue
        if is_procedural(sid):
            proc_skip += 1
        else:
            untranslated.append(s)

    print(
        f"Totale: {total} | Tradotte: {translated} | "
        f"Procedurali/skip: {proc_skip} | DA TRADURRE: {len(untranslated)}",
        file=sys.stderr
    )
    if stats_only:
        return

    lines = []
    for s in untranslated:
        ctx, sid = s.get('Context', ''), s.get('ID', '')
        val = s.get('Value')
        if val is not None:
            lines.append(f'  <string Context="{ctx}" ID="{sid}" Value="{val}" />')
        else:
            lines.append(f'  <string Context="{ctx}" ID="{sid}">{(s.text or "").strip()}</string>')

    out = "\n".join(lines)
    if output_path:
        open(output_path, 'w', encoding='utf-8').write(out)
        print(f"Scritto: {output_path} ({len(untranslated)} righe)", file=sys.stderr)
    else:
        print(out)


# ════════════════════════════════════════════════════════════════════════════
# MODALITÀ: pipeline  (tutto in un solo lancio)
#
#   Passo 1 — traduce: marca ogni stringa con ▶ e applica le traduzioni note
#             (match diretto + normalizzato, gestisce &#10; / \n / spazi)
#   Passo 2 — patch:   rilancia il matching su tutto il file per non perdere
#             nessuna voce che non era stata matchata al passo 1
#   Passo 3 — estrai:  stampa le statistiche e, se indicato, salva il report
#             delle stringhe ancora da tradurre
#
# Uso:
#   python coq_traduzioni.py pipeline INPUT.xml OUTPUT.xml [REPORT.txt] [--stats]
# ════════════════════════════════════════════════════════════════════════════
def cmd_pipeline(input_path, output_path, report_path=None, stats_only=False):
    print(f"\n{'='*60}")
    print(f"PIPELINE: {input_path} → {output_path}")
    print(f"{'='*60}")

    # ── Passo 1+2: unico passaggio in memoria ──────────────────────────────
    print("\n[1/2] Traduzione e patch...")
    tree = ET.parse(input_path)
    root = tree.getroot()
    strings = root.findall('string')
    total = len(strings)
    tradotte = 0

    for s in strings:
        sid = s.get('ID', '')
        orig = (s.get('Value') or s.text or '').strip()
        new_value = get_translated_value(sid, orig)
        if _lookup(sid) is not None:
            tradotte += 1
        _write_elem(s, new_value)

    print(f"    Stringhe totali : {total}")
    print(f"    Tradotte        : {tradotte}")
    print(f"    Non nel diz.    : {total - tradotte}")

    tree.write(output_path, encoding='utf-8', xml_declaration=True)
    check_n = len(ET.parse(output_path).getroot().findall('string'))
    print(f"    Verifica output : {check_n} stringhe — {'OK' if check_n == total else 'ERRORE!'}")

    # ── Passo 3: estrai non tradotte ───────────────────────────────────────
    print("\n[2/2] Estrazione stringhe non tradotte...")
    cmd_estrai(output_path, report_path, stats_only)

    print(f"\n{'='*60}")
    print("PIPELINE completata.")
    if report_path and not stats_only:
        print(f"Report non tradotte → {report_path}")
    print(f"{'='*60}\n")


# ════════════════════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════════════════════
USAGE = """\
Uso:
  python coq_traduzioni.py pipeline INPUT.xml OUTPUT.xml [REPORT.txt] [--stats]
      Esegue tutto in un lancio: traduzione completa + estrazione non tradotte.

  python coq_traduzioni.py traduce  INPUT.xml OUTPUT.xml
      Prima passata: aggiunge ▶ a tutte le stringhe e applica le traduzioni note.

  python coq_traduzioni.py patch    INPUT.xml OUTPUT.xml
      Patch selettivo: aggiorna solo le voci nel dizionario.

  python coq_traduzioni.py estrai   INPUT.xml [OUTPUT.txt] [--stats]
      Estrae le stringhe ancora non tradotte (valore == ID).
"""

if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        print(USAGE)
        sys.exit(1)

    cmd = args[0].lower()

    if cmd == 'pipeline':
        if len(args) < 3:
            print("Uso: python coq_traduzioni.py pipeline INPUT.xml OUTPUT.xml [REPORT.txt] [--stats]")
            sys.exit(1)
        stats = '--stats' in args
        positional = [a for a in args[1:] if a != '--stats']
        report = positional[2] if len(positional) > 2 else None
        cmd_pipeline(positional[0], positional[1], report, stats)

    elif cmd == 'traduce':
        if len(args) != 3:
            print("Uso: python coq_traduzioni.py traduce INPUT.xml OUTPUT.xml")
            sys.exit(1)
        cmd_traduce(args[1], args[2])

    elif cmd == 'patch':
        if len(args) != 3:
            print("Uso: python coq_traduzioni.py patch INPUT.xml OUTPUT.xml")
            sys.exit(1)
        cmd_patch(args[1], args[2])

    elif cmd == 'estrai':
        if len(args) < 2:
            print("Uso: python coq_traduzioni.py estrai INPUT.xml [OUTPUT.txt] [--stats]")
            sys.exit(1)
        stats = '--stats' in args
        positional = [a for a in args[1:] if a != '--stats']
        cmd_estrai(positional[0], positional[1] if len(positional) > 1 else None, stats)

    else:
        print(f"Comando sconosciuto: '{cmd}'\n{USAGE}")
        sys.exit(1)
