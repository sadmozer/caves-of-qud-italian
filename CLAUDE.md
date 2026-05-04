# Caves of Qud – Italian Localization Rules

## Context

This project contains Italian localization for *Caves of Qud*.

The system is procedural and uses:

* HistorySpice.json (dynamic templates)
* Strings.it.xml (localized strings)

Strings are recombined dynamically and are NOT static sentences.

## Critical Constraints

* The system does NOT handle gender correctly
* The system does NOT handle singular/plural correctly
* There are NO reliable helper functions for agreement
* NEVER use `|pluralize=`

## Goal

Do NOT translate.

Instead:

* Identify problematic Italian strings
* Rewrite them to be robust under ALL procedural combinations

## Hard Rules

* NEVER break or remove template syntax (=...=)
* NEVER hardcode values
* NEVER rely on singular/plural agreement
* NEVER rely on grammatical gender
* AVOID articles (il, lo, la, i, gli, le)
* AVOID adjectives that must agree

## Core Strategy (VERY IMPORTANT)

You MUST eliminate agreement entirely.

This means:

* No dependency on singular/plural
* No dependency on gender
* No fragile grammar

If a sentence depends on agreement → REWRITE IT

## Preferred Constructions

* verb-based structures
* impersonal forms
* neutral phrasing
* plural-safe verbs when possible
* restructuring instead of adapting

## Transformations

### 1. Abstract nouns → verbs

BAD: la protezione di X
GOOD: proteggono X / offrono protezione a X

---

### 2. Remove articles

BAD: il popolo di X
GOOD: popolo di X

---

### 3. Avoid adjectives

BAD: X è potente
GOOD: X dimostra potere

---

### 4. Break agreement chains

BAD: gli abitanti sono felici
GOOD: abitanti vivono in prosperità

---

### 5. Elliptical English → explicit Italian

Rewrite freely to achieve stability.

---

## Workflow (MANDATORY)

### Step 1 — Scan

Identify ONLY problematic lines:

* lines with templates (=...=)
* spice constructs
* sentences requiring agreement

Build an internal index.

Output ONLY:

* number of problematic lines
* short summary

DO NOT rewrite yet
DO NOT print full file

---

### Step 2 — Batch Fix

Process small batches (500 lines)
No unnecessary explanations
Use script or python scripts for operation (if needed)
---

### Step 3 — Quality Criteria

Each fix must:

* be stable in ALL combinations
* avoid gender/number agreement entirely
* preserve ALL templates exactly
* sound natural, slightly archaic, evocative

---

## Performance Rules

* Minimize output
* Never dump entire files
* Work incrementally

---

## Important Principle

If correct Italian requires agreement → DO NOT use that structure.

Rewrite instead.

Stability is more important than literal accuracy.
