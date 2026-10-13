"""Reproducible student registration-number dataset generator."""
import random
import re

def seed_from_registration(registration_number, fallback_seed=1234):
    digits = re.sub(r"\D", "", str(registration_number))
    return int(digits[-4:]) if len(digits) >= 4 else fallback_seed

def generate_dataset(n, seed, own_registration_number=None):
    rng = random.Random(seed)
    own = None
    try:
        own = int(re.sub(r"\D", "", str(own_registration_number)))
        if not str(own_registration_number).strip() or "ENTER" in str(own_registration_number):
            own = None
    except Exception:
        own = None
    # Keep the user's own registration number as a found test key; exclude own+1.
    values = set()
    if own is not None:
        values.add(own)
    while len(values) < n:
        value = rng.randint(100000, 999999999)
        if own is not None and value == own + 1:
            continue
        values.add(value)
    return sorted(values)
