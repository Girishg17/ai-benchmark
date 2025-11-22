import re

def numeric_match(ref: str, pred: str) -> bool:
    try:
        return float(ref) == float(pred)
    except:
        return False

def relaxed_match(ref: str, pred: str) -> bool:
    norm = lambda s: re.sub(r'[^a-z0-9]', '', s.lower())
    return norm(ref) in norm(pred)

def always_true(ref: str, pred: str) -> bool:
    return True
