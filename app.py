import streamlit as st
import nltk
from nltk.corpus import wordnet

# -----------------------------
# DOWNLOAD REQUIRED NLTK DATA
# -----------------------------
nltk.download("wordnet", quiet=True)
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)
nltk.download("averaged_perceptron_tagger_eng", quiet=True)

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="LexiScope - NLP Explorer",
    page_icon="📘",
    layout="wide"
)

# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown("""
<style>

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.main-title {
    font-size: 44px;
    font-weight: 700;
    margin-bottom: 0px;
}

.subtitle {
    font-size: 17px;
    color: #6c757d;
    margin-top: 5px;
    margin-bottom: 25px;
}

.word-box {
    padding: 20px;
    border-radius: 12px;
    background-color: rgba(120,120,120,0.08);
    border: 1px solid rgba(120,120,120,0.15);
    margin-top: 15px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# FUNCTIONS
# =========================================================

def get_synsets(word):
    return wordnet.synsets(word)


def get_definitions(word):
    definitions = []

    for syn in wordnet.synsets(word):
        if syn.definition():
            definitions.append(syn.definition())

    return list(dict.fromkeys(definitions))


def get_examples(word):
    examples = []

    for syn in wordnet.synsets(word):
        for example in syn.examples():

            if example:
                examples.append(example)

    return list(dict.fromkeys(examples))


def get_synonyms(word):
    synonyms = set()

    for syn in wordnet.synsets(word):

        for lemma in syn.lemmas():

            synonyms.add(
                lemma.name().replace("_", " ")
            )

    return sorted(synonyms)


def get_antonyms(word):
    antonyms = set()

    for syn in wordnet.synsets(word):

        for lemma in syn.lemmas():

            for antonym in lemma.antonyms():

                antonyms.add(
                    antonym.name().replace("_", " ")
                )

    return sorted(antonyms)


def get_hypernyms(word):
    hypernyms = set()

    for syn in wordnet.synsets(word):

        for hypernym in syn.hypernyms():

            for lemma in hypernym.lemmas():

                hypernyms.add(
                    lemma.name().replace("_", " ")
                )

    return sorted(hypernyms)


def get_hyponyms(word):
    hyponyms = set()

    for syn in wordnet.synsets(word):

        for hyponym in syn.hyponyms():

            for lemma in hyponym.lemmas():

                hyponyms.add(
                    lemma.name().replace("_", " ")
                )

    return sorted(hyponyms)


def get_meanings(word):
    meanings = []

    pos_names = {
        "n": "Noun",
        "v": "Verb",
        "a": "Adjective",
        "s": "Adjective",
        "r": "Adverb"
    }

    for syn in wordnet.synsets(word):

        meanings.append({
            "synset": syn.name(),
            "part_of_speech": pos_names.get(
                syn.pos(),
                syn.pos()
            ),
            "definition": syn.definition(),
            "examples": syn.examples()
        })

    return meanings


def calculate_similarity(word1, word2):

    synsets1 = wordnet.synsets(word1)
    synsets2 = wordnet.synsets(word2)

    if not synsets1 or not synsets2:
        return None

    best_similarity = 0

    for syn1 in synsets1:

        for syn2 in synsets2:

            similarity = syn1.wup_similarity(syn2)

            if similarity is not None:

                best_similarity = max(
                    best_similarity,
                    similarity
                )

    return best_similarity


# =========================================================
# POS DETAILS
# =========================================================

pos_meanings = {

    "CC": {
        "name": "Coordinating Conjunction",
        "explanation": "Words ya phrases ko join karta hai.",
        "example": "and, but, or"
    },

    "CD": {
        "name": "Cardinal Number",
        "explanation": "Number ya quantity show karta hai.",
        "example": "1, 20, hundred"
    },

    "DT": {
        "name": "Determiner",
        "explanation": "Noun se pehle aata hai aur noun ko specify karta hai.",
        "example": "a, an, the, this"
    },

    "EX": {
        "name": "Existential There",
        "explanation": "Kisi cheez ke existence ko show karta hai.",
        "example": "There is a book."
    },

    "FW": {
        "name": "Foreign Word",
        "explanation": "English ke ilawa kisi aur language ka word.",
        "example": "bonjour"
    },

    "IN": {
        "name": "Preposition / Subordinating Conjunction",
        "explanation": "Words ke darmiyan relationship show karta hai.",
        "example": "in, on, at, because"
    },

    "JJ": {
        "name": "Adjective",
        "explanation": "Noun ki quality ya characteristic describe karta hai.",
        "example": "beautiful, smart, large"
    },

    "JJR": {
        "name": "Comparative Adjective",
        "explanation": "Do cheezon ko compare karta hai.",
        "example": "bigger, faster, better"
    },

    "JJS": {
        "name": "Superlative Adjective",
        "explanation": "Highest degree of comparison show karta hai.",
        "example": "biggest, fastest, best"
    },

    "LS": {
        "name": "List Item Marker",
        "explanation": "List ke items ko indicate karta hai.",
        "example": "1., 2., A."
    },

    "MD": {
        "name": "Modal Verb",
        "explanation": "Ability, possibility, permission ya obligation show karta hai.",
        "example": "can, may, should, must"
    },

    "NN": {
        "name": "Singular Noun",
        "explanation": "Ek person, place, thing ya idea ka naam.",
        "example": "book, car, student"
    },

    "NNS": {
        "name": "Plural Noun",
        "explanation": "Ek se zyada persons, places ya things ko show karta hai.",
        "example": "books, cars, students"
    },

    "NNP": {
        "name": "Proper Noun",
        "explanation": "Kisi specific person, place ya organization ka naam.",
        "example": "Ali, Lahore, Google"
    },

    "NNPS": {
        "name": "Plural Proper Noun",
        "explanation": "Proper noun ka plural form.",
        "example": "Americans, Smiths"
    },

    "PDT": {
        "name": "Predeterminer",
        "explanation": "Determiner se pehle use hota hai.",
        "example": "all, both, half"
    },

    "POS": {
        "name": "Possessive Ending",
        "explanation": "Ownership show karta hai.",
        "example": "Ali's book"
    },

    "PRP": {
        "name": "Personal Pronoun",
        "explanation": "Noun ki jagah use hota hai.",
        "example": "I, you, he, she, they"
    },

    "PRP$": {
        "name": "Possessive Pronoun",
        "explanation": "Ownership show karta hai.",
        "example": "my, your, his, their"
    },

    "RB": {
        "name": "Adverb",
        "explanation": "Verb, adjective ya kisi aur adverb ko describe karta hai.",
        "example": "quickly, very, slowly"
    },

    "RBR": {
        "name": "Comparative Adverb",
        "explanation": "Do actions ya qualities ko compare karta hai.",
        "example": "faster, better"
    },

    "RBS": {
        "name": "Superlative Adverb",
        "explanation": "Highest degree of an action show karta hai.",
        "example": "fastest, best"
    },

    "RP": {
        "name": "Particle",
        "explanation": "Verb ke saath mil kar phrasal verb banata hai.",
        "example": "give up, turn off"
    },

    "SYM": {
        "name": "Symbol",
        "explanation": "Special ya mathematical symbol.",
        "example": "+, %, ="
    },

    "TO": {
        "name": "To",
        "explanation": "Infinitive ya direction ke liye use hota hai.",
        "example": "to go, to school"
    },

    "UH": {
        "name": "Interjection",
        "explanation": "Emotion ya reaction express karta hai.",
        "example": "wow, oh, hey"
    },

    "VB": {
        "name": "Verb - Base Form",
        "explanation": "Verb ki basic form hoti hai.",
        "example": "go, eat, write"
    },

    "VBD": {
        "name": "Verb - Past Tense",
        "explanation": "Past mein hone wale action ko show karta hai.",
        "example": "went, ate, played"
    },

    "VBG": {
        "name": "Verb - Gerund / Present Participle",
        "explanation": "Usually verb ki -ing form hoti hai.",
        "example": "reading, playing, running"
    },

    "VBN": {
        "name": "Verb - Past Participle",
        "explanation": "Perfect tense ya passive voice mein use hota hai.",
        "example": "written, eaten, gone"
    },

    "VBP": {
        "name": "Verb - Present Tense",
        "explanation": "Present tense mein I, you, we, they ke saath commonly use hota hai.",
        "example": "I eat, they play"
    },

    "VBZ": {
        "name": "Verb - 3rd Person Singular Present",
        "explanation": "Present tense mein he, she ya it ke saath use hota hai.",
        "example": "he eats, she runs"
    },

    "WDT": {
        "name": "Wh-Determiner",
        "explanation": "Question ya relative clause mein noun ko determine karta hai.",
        "example": "which, whatever"
    },

    "WP": {
        "name": "Wh-Pronoun",
        "explanation": "Question mein person ya thing ke liye use hota hai.",
        "example": "who, what"
    },

    "WP$": {
        "name": "Possessive Wh-Pronoun",
        "explanation": "Question mein ownership poochta hai.",
        "example": "whose"
    },

    "WRB": {
        "name": "Wh-Adverb",
        "explanation": "Question mein place, time ya reason poochta hai.",
        "example": "where, when, why"
    }
}


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("📘 LexiScope")

    st.caption(
        "WordNet and NLP exploration tool."
    )

    st.divider()

    st.subheader("Features")

    st.write("📘 Definitions")
    st.write("💬 Examples")
    st.write("🔄 Synonyms")
    st.write("↔️ Antonyms")
    st.write("⬆️ Hypernyms")
    st.write("⬇️ Hyponyms")
    st.write("🧠 Meanings")
    st.write("✂️ Tokenization")
    st.write("🏷️ Detailed Parts of Speech")
    st.write("⚖️ Word Similarity")


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">📚 LexiScope</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
    Explore words and perform basic NLP analysis using NLTK and WordNet
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# MAIN TABS
# =========================================================

main_tabs = st.tabs([
    "📖 WordNet Explorer",
    "✂️ Tokenization",
    "🏷️ Parts of Speech",
    "⚖️ Similarity Comparison"
])


# =========================================================
# TAB 1 - WORDNET EXPLORER
# =========================================================

with main_tabs[0]:

    word = st.text_input(
        "Enter an English word:",
        placeholder="Example: bank, car, happy"
    )

    word = word.strip().lower()

    if word:

        synsets = get_synsets(word)

        if not synsets:

            st.error(
                f'No WordNet information found for "{word}".'
            )

        else:

            definitions = get_definitions(word)
            examples = get_examples(word)
            synonyms = get_synonyms(word)
            antonyms = get_antonyms(word)
            hypernyms = get_hypernyms(word)
            hyponyms = get_hyponyms(word)
            meanings = get_meanings(word)

            st.markdown(
                f"""
                <div class="word-box">

                    <div style="font-size:14px; opacity:0.7;">
                        Search Result
                    </div>

                    <div style="font-size:30px; font-weight:700;">
                        {word.title()}
                    </div>

                    <div style="font-size:14px; opacity:0.7;">
                        {len(meanings)} meaning(s) found
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

            st.write("")

            m1, m2, m3, m4 = st.columns(4)

            m1.metric("Meanings", len(meanings))
            m2.metric("Synonyms", len(synonyms))
            m3.metric("Antonyms", len(antonyms))
            m4.metric("Examples", len(examples))

            word_tabs = st.tabs([
                "Overview",
                "Definitions",
                "Examples",
                "Synonyms",
                "Antonyms",
                "Hypernyms",
                "Hyponyms",
                "Meanings"
            ])

            # OVERVIEW
            with word_tabs[0]:

                if definitions:

                    st.subheader("Primary Definition")
                    st.info(definitions[0])

                col1, col2 = st.columns(2)

                with col1:

                    st.subheader("Synonyms")

                    if synonyms:
                        st.write(
                            ", ".join(synonyms[:10])
                        )

                    else:
                        st.write("No synonyms found.")

                with col2:

                    st.subheader("Antonyms")

                    if antonyms:
                        st.write(
                            ", ".join(antonyms[:10])
                        )

                    else:
                        st.write("No antonyms found.")


            # DEFINITIONS
            with word_tabs[1]:

                st.subheader("📘 Definitions")

                if definitions:

                    for i, definition in enumerate(
                        definitions,
                        start=1
                    ):

                        with st.container(border=True):

                            st.markdown(
                                f"**Definition {i}**"
                            )

                            st.write(definition)

                else:
                    st.warning(
                        "No definitions found."
                    )


            # EXAMPLES
            with word_tabs[2]:

                st.subheader("💬 Examples")

                if examples:

                    for i, example in enumerate(
                        examples,
                        start=1
                    ):

                        with st.container(border=True):

                            st.markdown(
                                f"**Example {i}**"
                            )

                            st.write(example)

                else:

                    st.warning(
                        "No examples available."
                    )


            # SYNONYMS
            with word_tabs[3]:

                st.subheader("🔄 Synonyms")

                if synonyms:

                    for item in synonyms:
                        st.write("•", item)

                else:

                    st.warning(
                        "No synonyms found."
                    )


            # ANTONYMS
            with word_tabs[4]:

                st.subheader("↔️ Antonyms")

                if antonyms:

                    for item in antonyms:
                        st.write("•", item)

                else:

                    st.warning(
                        "No antonyms found."
                    )


            # HYPERNYMS
            with word_tabs[5]:

                st.subheader("⬆️ Hypernyms")

                st.caption(
                    "Broader categories"
                )

                if hypernyms:

                    for item in hypernyms:
                        st.write("•", item)

                else:

                    st.warning(
                        "No hypernyms found."
                    )


            # HYPONYMS
            with word_tabs[6]:

                st.subheader("⬇️ Hyponyms")

                st.caption(
                    "More specific categories"
                )

                if hyponyms:

                    for item in hyponyms:
                        st.write("•", item)

                else:

                    st.warning(
                        "No hyponyms found."
                    )


            # DIFFERENT MEANINGS
            with word_tabs[7]:

                st.subheader(
                    "🧠 Different Meanings"
                )

                for i, meaning in enumerate(
                    meanings,
                    start=1
                ):

                    with st.expander(
                        f"Meaning {i} - "
                        f"{meaning['part_of_speech']}"
                    ):

                        st.write(
                            "**Definition:**",
                            meaning["definition"]
                        )

                        if meaning["examples"]:

                            st.write(
                                "**Examples:**"
                            )

                            for example in meaning["examples"]:
                                st.write(
                                    "•",
                                    example
                                )

                        else:

                            st.caption(
                                "No example available."
                            )


# =========================================================
# TAB 2 - TOKENIZATION
# =========================================================

with main_tabs[1]:

    st.header("✂️ Tokenization")

    st.write(
        "Tokenization breaks a sentence into individual words and punctuation."
    )

    sentence = st.text_area(
        "Enter a sentence:",
        placeholder="Example: Ali has 2 books and 5 pens."
    )

    if st.button(
        "Tokenize Sentence",
        key="token_button"
    ):

        if sentence.strip():

            tokens = nltk.word_tokenize(
                sentence
            )

            st.subheader(
                "Tokens"
            )

            st.write(tokens)

            st.metric(
                "Total Tokens",
                len(tokens)
            )

        else:

            st.warning(
                "Please enter a sentence."
            )


# =========================================================
# TAB 3 - DETAILED PARTS OF SPEECH
# =========================================================

with main_tabs[2]:

    st.header(
        "🏷️ Detailed Parts of Speech Analysis"
    )

    st.write(
        "Enter a sentence to identify and explain the part of speech of every word."
    )

    pos_sentence = st.text_area(
        "Enter a sentence for POS tagging:",
        placeholder="Example: Ali is reading a beautiful book."
    )

    if st.button(
        "Analyze Parts of Speech",
        key="pos_button"
    ):

        if pos_sentence.strip():

            tokens = nltk.word_tokenize(
                pos_sentence
            )

            tags = nltk.pos_tag(
                tokens
            )

            st.subheader(
                "Detailed POS Analysis"
            )

            for word_item, tag in tags:

                information = pos_meanings.get(
                    tag
                )

                with st.container(
                    border=True
                ):

                    st.markdown(
                        f"### {word_item}"
                    )

                    col1, col2 = st.columns(2)

                    with col1:

                        st.write(
                            "**POS Tag:**",
                            tag
                        )

                        if information:

                            st.write(
                                "**Part of Speech:**",
                                information["name"]
                            )

                    with col2:

                        if information:

                            st.write(
                                "**Example:**",
                                information["example"]
                            )

                    if information:

                        st.write(
                            "**Explanation:**",
                            information["explanation"]
                        )

                    else:

                        st.write(
                            "**Part of Speech:** "
                            "Punctuation / Special Symbol"
                        )


            # ---------------------------------
            # SUMMARY TABLE
            # ---------------------------------

            st.subheader(
                "POS Summary"
            )

            table_data = []

            for word_item, tag in tags:

                information = pos_meanings.get(
                    tag
                )

                if information:

                    name = information["name"]

                else:

                    name = "Punctuation / Symbol"

                table_data.append({
                    "Word": word_item,
                    "POS Tag": tag,
                    "Part of Speech": name
                })

            st.dataframe(
                table_data,
                use_container_width=True
            )

        else:

            st.warning(
                "Please enter a sentence."
            )


# =========================================================
# TAB 4 - SIMILARITY COMPARISON
# =========================================================

with main_tabs[3]:

    st.header(
        "⚖️ Word Similarity Comparison"
    )

    st.write(
        "Compare the semantic similarity of two words using WordNet Wu-Palmer Similarity."
    )

    col1, col2 = st.columns(2)

    with col1:

        word1 = st.text_input(
            "First Word",
            placeholder="Example: car"
        )

    with col2:

        word2 = st.text_input(
            "Second Word",
            placeholder="Example: bus"
        )

    if st.button(
        "Compare Similarity",
        key="similarity_button"
    ):

        word1 = word1.strip().lower()
        word2 = word2.strip().lower()

        if word1 and word2:

            similarity = calculate_similarity(
                word1,
                word2
            )

            if similarity is None:

                st.error(
                    "One or both words were not found in WordNet."
                )

            else:

                percentage = (
                    similarity * 100
                )

                st.metric(
                    "Similarity Score",
                    f"{percentage:.2f}%"
                )

                st.progress(
                    int(percentage)
                )

                if percentage >= 80:

                    st.success(
                        "The words are highly similar."
                    )

                elif percentage >= 50:

                    st.info(
                        "The words are moderately similar."
                    )

                else:

                    st.warning(
                        "The words have low semantic similarity."
                    )

        else:

            st.warning(
                "Please enter both words."
            )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "LexiScope | NLP Explorer | Built with Streamlit, NLTK and WordNet"
)
