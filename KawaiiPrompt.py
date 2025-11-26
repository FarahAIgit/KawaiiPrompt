import streamlit as st
import random
import itertools

st.set_page_config(page_title="Kawaii Prompt Generator", layout="wide")

# ---------------------------
# Kawaii pastel styling
# ---------------------------
st.markdown(
    """
    <style>
    body { background-color: #fff5f8; color: #2d1b3d; font-family: 'Comic Sans MS', 'Chalkboard SE', 'Comic Neue', cursive; }
    .stApp { min-height: 100vh; background: linear-gradient(135deg, #fff5f8 0%, #ffe8f0 50%, #f0f8ff 100%); }
    .stTextArea textarea { background: rgba(255,255,255,0.95); color: #d946b0; border: 2px solid #ffb6d9; border-radius: 15px; }
    .stButton>button { 
        background: linear-gradient(135deg, #ff69b4 0%, #ff8dc7 100%); 
        color: white; 
        border-radius: 20px; 
        padding: 10px 20px;
        border: 3px solid #ff69b4;
        font-weight: bold;
        box-shadow: 0 4px 10px rgba(255, 105, 180, 0.4);
        font-size: 16px;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #ff8dc7 0%, #ffa8d9 100%);
        transform: scale(1.05);
    }
    .block-container { padding: 1rem 2rem; }
    h1,h2,h3 { 
        color: #d946b0 !important; 
        font-family: 'Comic Sans MS', cursive;
        text-shadow: 2px 2px 4px rgba(255, 182, 217, 0.6);
        font-weight: bold;
    }
    h2 {
        color: #d946b0 !important;
        font-size: 1.8em !important;
    }
    .footer { color: #d946b0; font-size: 12px; margin-top: 8px; }
    .stCodeBlock { 
        background: rgba(255, 255, 255, 0.95); 
        border: 3px solid #ff69b4;
        border-radius: 15px;
    }
    .stCodeBlock code { 
        white-space: pre-wrap !important; 
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        color: #d946b0;
        font-weight: 500;
    }
    .stCodeBlock pre {
        white-space: pre-wrap !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        overflow-x: auto !important;
    }
    [data-testid="stCode"] {
        white-space: pre-wrap !important;
    }
    [data-testid="stCode"] code {
        white-space: pre-wrap !important;
        word-wrap: break-word !important;
    }
    .stCheckbox input[type="checkbox"]:checked {
        background-color: #ff69b4 !important;
        border-color: #ff69b4 !important;
    }
    .stCheckbox [data-testid="stCheckbox"] input:checked ~ span {
        background-color: #ff69b4 !important;
        border-color: #ff69b4 !important;
    }
    .stCheckbox label {
        background-color: transparent !important;
        color: #2d1b3d !important;
        font-weight: 500;
    }
    .stCheckbox span {
        background-color: transparent !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("### 🌸✨ Kawaii Prompt Generator ✨🌸", unsafe_allow_html=True)
st.markdown("*A magical cuteness engine* 💕")
st.markdown("---")

# Add CSS to center the title and tagline
st.markdown(
    """
    <style>
    .block-container > div > div > div:first-child h3 {
        text-align: center;
        color: #d946b0 !important;
    }
    .block-container > div > div > div:first-child p {
        text-align: center;
        color: #2d1b3d !important;
        font-weight: 500;
    }
    /* Make all paragraph text darker */
    p, .stMarkdown p {
        color: #2d1b3d !important;
    }
    /* Make markdown text darker */
    .stMarkdown {
        color: #2d1b3d !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------
# Time-related words pool (kawaii version)
# ---------------------------
TIME_WORDS = [
    "on a sunny morning", "during golden hour", "at playtime", "in springtime forever",
    "on a rainbow day", "during teatime", "at the magic hour", "in dreamland",
    "on a sparkly afternoon", "during cherry blossom season", "at sunrise",
    "in a candy-colored moment", "on the brightest day", "during starlight",
    "at moonbeam hour", "in a bubblegum dream", "on a cupcake morning",
    "during butterfly time", "at the happiest moment", "in cookie heaven",
    "on a giggle-filled day", "during cotton candy clouds", "at adventure time",
    "in a fairy tale", "on a bouncy day", "during smile time", "at the festival",
    "in a snow globe", "on Valentine's morning", "during the friendship hour"
]

# ---------------------------
# Kawaii person descriptor pool
# ---------------------------
PERSON_BASE_DESCRIPTORS = [
    "cheerful character", "adorable friend", "happy companion", "bubbly soul",
    "gentle dreamer", "sweet friend", "joyful spirit", "playful wanderer",
    "kind-hearted explorer", "magical friend", "chibi adventurer", "cute traveler",
    "smiling person", "bouncy character", "sparkly individual", "fluffy friend",
    "rainbow seeker", "cupcake lover", "starry-eyed dreamer", "button-nosed cutie",
    "rosy-cheeked friend", "twinkle-eyed wanderer", "giggling companion",
    "the happiness spreader", "the joy bringer", "the cuddle expert",
    "the smile maker", "the friend collector", "the dream believer"
]

PERSON_STYLE_MODIFIERS = [
    "wearing pastel overalls", "in a fluffy sweater", "with rainbow accessories",
    "dressed in polka dots", "wearing a flower crown", "in striped socks",
    "with cute hairclips", "wearing bunny ears", "in a frilly dress",
    "with sparkling shoes", "wearing star patterns", "in cozy pajamas",
    "with heart-shaped glasses", "wearing kawaii fashion", "in candy colors",
    "with a bow tie", "wearing magical girl outfit", "in fairy wings"
]

# ---------------------------
# Programmatic generation of 1000 kawaii words
# ---------------------------
base_nouns = [
    "rainbow","bubble","cupcake","cookie","candy","sprinkle","starlight","moonbeam","sunshine","cloud",
    "flower","blossom","petal","butterfly","bunny","kitten","puppy","hamster","bear","panda",
    "unicorn","fairy","angel","heart","star","moon","sun","sky","garden","meadow",
    "cherry","peach","strawberry","melon","apple","berry","honey","sugar","cream","frosting",
    "ribbon","bow","lace","button","pearl","gem","crystal","diamond","sparkle","glitter",
    "balloon","confetti","party","celebration","smile","giggle","laugh","joy","happiness","dream",
    "wish","hope","magic","wonder","miracle","friendship","love","kindness","warmth","comfort",
    "teddy","plushie","toy","doll","teacup","teapot","cupcake","muffin","donut","macaron",
    "lollipop","marshmallow","jellybean","gumdrop","caramel","vanilla","chocolate","mint","sherbet","sorbet",
    "cottage","castle","treehouse","playground","carousel","ferris wheel","swing","slide","sandbox","garden",
    "pond","stream","waterfall","fountain","dewdrop","snowflake","raindrop","sunbeam","aurora","comet",
    "feather","wing","nest","birdhouse","acorn","pinecone","leaf","clover","daisy","tulip",
    "rose","lily","orchid","jasmine","lavender","poppy","dandelion","sunflower","cosmos","peony",
    "bluebell","violet","pansy","iris","magnolia","sakura","wisteria","hydrangea","carnation","daffodil"
]

mods = [
    "adorable","bubbly","cheerful","cozy","cute","dreamy","fluffy","friendly","gentle","happy",
    "joyful","lovely","magical","pastel","playful","pretty","rainbow","rosy","shiny","soft",
    "sparkling","sweet","tiny","twinkling","warm","bouncy","chubby","dainty","fuzzy","glossy",
    "glowing","kawaii","peachy","perky","plush","puffy","round","silly","smiling","snuggly"
]

extras = [
    "bubblegum","cotton candy","fairy floss","gummy","jelly","latte","milkshake","pudding","smoothie","waffle",
    "pancake","biscuit","scone","tart","pie","cake","icing","topping","whipped cream","syrup",
    "polka dot","stripe","pattern","print","design","motif","icon","emoji","sticker","stamp",
    "gloss","shimmer","shine","glow","twinkle","flash","beam","ray","halo","aura",
    "melody","tune","song","chime","bell","whistle","giggle","chirp","tweet","purr",
    "hug","cuddle","snuggle","nuzzle","smooch","wink","peace sign","thumbs up","high five","wave",
    "picnic","teatime","party","sleepover","playdate","festival","carnival","fair","parade","celebration",
    "surprise","present","gift","treasure","keepsake","memento","souvenir","trinket","charm","token",
    "pocket","pouch","purse","bag","basket","box","jar","bottle","container","wrapper",
    "note","letter","card","postcard","invitation","bookmark","diary","journal","scrapbook","album"
]

def build_word_pool(target=1000):
    pool = []
    pool.extend(base_nouns)
    pool.extend(extras)
    for a, b in itertools.product(mods, base_nouns):
        pool.append(f"{a} {b}")
        if len(pool) >= target:
            break
    if len(pool) < target:
        for a, b in itertools.product(mods, extras):
            pool.append(f"{a} {b}")
            if len(pool) >= target:
                break
    uniq = []
    for w in pool:
        if w not in uniq:
            uniq.append(w)
        if len(uniq) >= target:
            break
    return uniq

KAWAII_WORDS = build_word_pool(1000)

# ========================================
# PURE KAWAII MODE - PROCEDURAL WORD GENERATION
# ========================================

def generate_kawaii_word():
    """Generate cute-sounding made-up words using kawaii syllable patterns"""
    # Cute consonant sounds
    consonants = ['k', 'p', 'n', 'm', 'r', 'y', 'ch', 'w', 'h', 's']
    consonant_clusters = ['ky', 'py', 'ny', 'my', 'ry', 'ch', 'sh', 'tw', 'fl', 'pl', 'pr', 'sw']
    
    # Cute vowel combinations
    vowels = ['a', 'i', 'u', 'e', 'o', 'ee', 'oo', 'ai', 'ie', 'ui']
    
    # Cute endings
    endings = ['', 'n', 'ko', 'chi', 'pi', 'mi', 'ri', 'ki', 'shi', 'tte', 'ppu']
    
    # Generate 2-3 syllables for maximum cuteness
    num_syllables = random.choice([2, 2, 3])  # Weighted toward 2
    word = ""
    
    for i in range(num_syllables):
        # Start with consonant or cluster
        if random.random() < 0.3:
            word += random.choice(consonant_clusters)
        else:
            word += random.choice(consonants)
        
        # Add vowel
        word += random.choice(vowels)
        
        # Add ending (more likely on last syllable)
        if i == num_syllables - 1:
            if random.random() < 0.5:
                word += random.choice(endings)
        else:
            if random.random() < 0.1:
                word += random.choice(endings)
    
    return word

def mix_kawaii_words(word_list, kawaii_percentage=0.4):
    """Replace a percentage of real words with procedurally generated cute ones"""
    num_kawaii = int(len(word_list) * kawaii_percentage)
    num_real = len(word_list) - num_kawaii
    
    real_words = random.sample(KAWAII_WORDS, num_real)
    kawaii_words = [generate_kawaii_word() for _ in range(num_kawaii)]
    
    mixed = real_words + kawaii_words
    random.shuffle(mixed)
    
    return mixed

# ========================================
# END PURE KAWAII MODE SECTION
# ========================================

VISUAL_DESCRIPTORS = [
    "soft pastel colors","gentle light bloom","floating cotton candy clouds","rainbow reflections",
    "bouncy animation","cute sparkle effects","bubbly textures","magical girl transformation",
    "glitter particles everywhere","heart-shaped bokeh","twinkling star effects","soft focus glow",
    "kawaii chibi proportions","bright happy colors","cheerful gradients","playful motion blur",
    "candy-coated aesthetic","dreamy soft lighting","whimsical floating elements","adorable details"
]

MJ_STYLIZE_VALUES = [50, 100, 250, 500, 625, 750, 1000]

def make_prompt(person_mode=False, add_mj_params=True, pure_kawaii_mode=False, add_time=False):
    if pure_kawaii_mode:
        word_source = mix_kawaii_words(list(range(15)), kawaii_percentage=0.5)
        fragments = word_source
    else:
        fragments = random.sample(KAWAII_WORDS, k=15)
    
    all_individual_words = []
    unique_fragments = []
    
    for fragment in fragments:
        fragment_str = str(fragment)
        words_in_fragment = fragment_str.lower().split()
        has_duplicate = any(word in all_individual_words for word in words_in_fragment)
        
        if not has_duplicate:
            unique_fragments.append(fragment_str)
            all_individual_words.extend(words_in_fragment)
        
        if len(unique_fragments) >= 9:
            break
    
    while len(unique_fragments) < 9:
        if pure_kawaii_mode:
            new_fragment = generate_kawaii_word()
        else:
            new_fragment = random.choice(KAWAII_WORDS)
        if new_fragment not in unique_fragments:
            unique_fragments.append(new_fragment)
    
    body_words = unique_fragments[0:3]
    hint_words = unique_fragments[3:6]
    person_candidates = unique_fragments[6:9]
    
    person_base = random.choice(PERSON_BASE_DESCRIPTORS)
    if random.random() < 0.5:
        person_style = random.choice(PERSON_STYLE_MODIFIERS)
        person_phrase = f"{person_base} {person_style}"
    else:
        person_phrase = person_base

    time_phrase = ""
    if add_time:
        time_phrase = f", {random.choice(TIME_WORDS)},"

    if person_mode:
        prompt_body = (
            f"A {person_phrase}{time_phrase} playing among {body_words[0]}, {body_words[1]}, {body_words[2]}, "
            f"with hints of {hint_words[0]}, {hint_words[1]}, {hint_words[2]}, "
            f"{random.choice(VISUAL_DESCRIPTORS)}"
        )
    else:
        prompt_body = (
            f"A {body_words[0]} {body_words[1]}{time_phrase} surrounded by {body_words[2]}, "
            f"with {hint_words[0]}, {hint_words[1]}, {hint_words[2]}, "
            f"{random.choice(VISUAL_DESCRIPTORS)}"
        )

    if add_mj_params:
        s_val = random.choice(MJ_STYLIZE_VALUES)
        sref_val = random.randint(0, 4294967295)
        prompt_body += f" --s {s_val} --sref {sref_val}"

    return prompt_body

# ---------------------------
# Streamlit UI
# ---------------------------
if "prompt" not in st.session_state:
    st.session_state.prompt = ""

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("## Options 🎀")
    person_mode = st.checkbox("Center the prompt around a person 👤", value=False)
    add_mj = st.checkbox("Add random MidJourney --s and --sref ⚙️", value=True)
    add_time = st.checkbox("⏰ Add time element", value=False)
    pure_kawaii = st.checkbox("🌈 Pure Kawaii Mode (generate cute invented words)", value=False)
    if st.button("Generate Prompt ✨"):
        st.session_state.prompt = make_prompt(person_mode, add_mj_params=add_mj, pure_kawaii_mode=pure_kawaii, add_time=add_time)
    st.markdown("---")
    st.markdown(
    "<p style='color: #2d1b3d; font-weight: 600;'>Created with 💕 by <a href='https://x.com/Farah_ai_' style='color: #d946b0; font-weight: 700;'>@Farah_ai_</a></p>", unsafe_allow_html=True)

with col2:
    st.markdown("## Output 🎨")
    if st.session_state.prompt:
        st.markdown("<p style='color: #2d1b3d; font-weight: 600;'><strong style='color: #d946b0;'>Your Kawaii Prompt</strong> <em>(click the copy icon in the top-right corner):</em></p>", unsafe_allow_html=True)
        st.code(st.session_state.prompt, language=None)

st.markdown("<p style='color: #2d1b3d; font-weight: 600;'>💡 Tip: Click the copy icon (top right of the prompt box) to copy your prompt!</p>", unsafe_allow_html=True)
st.markdown("---")
st.markdown(
    "<p style='color: #2d1b3d; font-weight: 600;'>Use of this generator is free but if you find it useful please consider donating a little; <a href='https://ko-fi.com/farahai' style='color: #d946b0; font-weight: 700;'>Donate via Kofi ☕</a></p>",
    unsafe_allow_html=True
)
st.markdown("<p style='color: #d946b0; font-weight: 700; font-style: italic; text-align: center;'>~ Spread the kawaii magic! ~ ✨💖</p>", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    .block-container {
        backdrop-filter: blur(6px);
        background: rgba(255, 255, 255, 0.85);
        border-radius: 20px;
        padding: 30px;
        border: 3px solid #ff69b4;
        box-shadow: 0 8px 20px rgba(255, 105, 180, 0.3);
    }
    </style>
    """,
    unsafe_allow_html=True
)
