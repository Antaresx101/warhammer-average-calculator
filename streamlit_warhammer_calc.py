import streamlit as st
import re

def parse_expression(expr):
    match = re.match(r"(\d+)xBS(\d\+)?/S(\d+)/(-?\d+)/(\d+)vsT(\d+)/(\d\+)", expr.replace(" ", ""))
    if not match:
        return None
    shots, bs, s, ap, dmg, t, save = match.groups()
    return {
        "shots": int(shots),
        "bs": int(bs[:-1]),
        "s": int(s),
        "ap": int(ap),
        "dmg": int(dmg),
        "t": int(t),
        "save": int(save[:-1])
    }

def hit_chance(bs):
    return max(0, (7 - bs)) / 6

def wound_chance(s, t):
    if s >= 2 * t:
        return 5/6
    elif s > t:
        return 4/6
    elif s == t:
        return 3/6
    elif s * 2 <= t:
        return 1/6
    else:
        return 2/6

def save_chance(save, ap):
    modified = save + ap
    if modified >= 7:
        return 0
    return (7 - modified) / 6

def calculate_wounds(data):
    hits = data["shots"] * hit_chance(data["bs"])
    wounds = hits * wound_chance(data["s"], data["t"])
    unsaved = wounds * (1 - save_chance(data["save"], data["ap"]))
    total_damage = unsaved * data["dmg"]
    return round(total_damage, 2)

# UI
query = st.st.query_params()
expr = query.get("q", [""])[0]

st.title("Warhammer 40k Average Calculator")

if expr:
    st.write(f"**Query:** `{expr}`")
    data = parse_expression(expr)
    if data:
        result = calculate_wounds(data)
        st.write(f"**Estimated Damage:** `{result}`")
    else:
        st.error("Invalid expression. Use format like: `20x BS3+/S4/-1/1 vs T5/3+`")
else:
    st.write("Add `?q=...` to the URL to get started.")
