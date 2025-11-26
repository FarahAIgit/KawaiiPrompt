import streamlit as st
import requests
import random

st.title("Hybrid Random Prompt Generator")
st.write("A surreal prompt generator powered by chaos, poetry, and optional human focus.")

# Random Word API URL
RANDOM_WORD_URL = "https://random-word-api.herokuapp.com/word?number=3"

# Datamuse API
DATAMUSE_URL = "https://api.datamuse.com/words?ml="

def get_random_words():
    try:
        r = requests.get(RANDOM_WORD_URL, timeout=5)
        if r.status_code == 200:
            return r.json()
        return ["ghost", "signal", "static"]  # fallback
    except:
        return ["shadow", "glass", "orbit"]

def get_related_words(word):
    try:
        r = requests.get(DATAMUSE_URL + word, timeout=5)
        if r.status_code == 200:
            words = [item["word"] for item in r.json()]
            return words[:10] if words else []
        return []
    except:
        return []

# Human descriptors for fallback or flavor
human_adj = [
    "mysterious", "ethereal", "surreal", "dreamlike", "eerie",
    "otherworldly", "luminous", "ageless", "enigmatic", "soft-lit"
]

def make_prompt(person_mode=False):
    base_words = get_random_words()
    trigger_word = random.choice(base_words)
    related = get_related_words(trigger_word)

    flavour = random.sample(related, k=min(len(related), random.randint(1, 2))) if related else []
    fragments = base_words + flavour
    random.shuffle(fragments)

    if person_mode:
        # Try using one related word as personality or aesthetic flavour
        person_flavour = random.choice(flavour) if flavour else random.choice(human_adj)

        prompt = (
            f"A {person_flavour} person standing among {fragments[0]}, {fragments[1]}, and {fragments[2]}, "
            f"with hints of {', '.join(fragments[3:]) if len(fragments) > 3 else 'ambient static'}, "
            f"cinematic lighting and surreal atmospheric tones."
        )
    else:
        prompt = (
            f"A {fragments[0]} {fragments[1]} emerging from {fragments[2]}, "
            f"surrounded by {', '.join(fragments[3:]) if len(fragments) > 3 else 'ambient static'}, "
            f"cinematic lighting and strange dreamlike atmosphere."
        )

    return prompt


# UI toggle
person_mode = st.checkbox("Center the prompt around a person", value=False)

if st.button("Generate Prompt"):
    st.success(make_prompt(person_mode))

# Footer
st.markdown(
    "Created by [@YourTwitterName](https://twitter.com/YourTwitterName)",
    unsafe_allow_html=True
)
