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

# -----------------------------
# FUNCTIONS
# -----------------------------
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
                syn.pos(), syn.pos()
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


# -----------------------------
# POS TAG MEANINGS
# -----------------------------
pos_meanings = {
    "CC": "Coordinating conjunction",
    "CD": "Cardinal number",
    "DT": "Determiner",
    "EX": "Existential there",
    "FW": "Foreign word",
    "IN": "Preposition or subordinating conjunction",
    "JJ": "Adjective",
    "JJR": "Comparative adjective",
    "JJS": "Superlative adjective",
    "LS": "List item marker",
    "MD": "Modal verb",
    "NN": "Singular noun",
    "NNS": "Plural noun",
    "NNP": "Singular proper noun",
    "NNPS": "Plural proper noun",
    "PDT": "Predeterminer",
    "POS": "Possessive ending",
    "PRP": "Personal pronoun",
    "PRP$": "Possessive pronoun",
    "RB": "Adverb",
    "RBR": "Comparative adverb",
    "RBS": "Superlative adverb",
    "RP": "Particle",
    "SYM": "Symbol",
    "TO": "To",
    "UH": "Interjection",
    "VB": "Verb, base form",
    "VBD": "Verb, past tense",
    "VBG": "Verb, gerund or present participle",
    "VBN": "Verb, past participle",
    "VBP": "Verb, present tense",
    "VBZ": "Verb, 3rd person singular present",
    "WDT": "Wh-determiner",
    "WP": "Wh-pronoun",
    "WP$": "Possessive wh-pronoun",
    "WRB": "Wh-adverb"
}


# -----------------------------
# SIDEBAR
# -----------------------------
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
    st.write("🏷️ Parts of Speech")
    st.write("⚖️ Word Similarity")


# -----------------------------
# HEADER
# -----------------------------
st.markdown(
    '<div class="main-title">📚 LexiScope</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
    Explore words and perform basic NLP analysis using NLTK
    </div>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# MAIN TABS
# -----------------------------
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
                    st.warning("No definitions found.")


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
                    st.warning("No synonyms found.")


            # ANTONYMS
            with word_tabs[4]:

                st.subheader("↔️ Antonyms")

                if antonyms:

                    for item in antonyms:
                        st.write("•", item)

                else:
                    st.warning("No antonyms found.")


            # HYPERNYMS
            with word_tabs[5]:

                st.subheader("⬆️ Hypernyms")
                st.caption("Broader categories")

                if hypernyms:

                    for item in hypernyms:
                        st.write("•", item)

                else:
                    st.warning("No hypernyms found.")


            # HYPONYMS
            with word_tabs[6]:

                st.subheader("⬇️ Hyponyms")
                st.caption("More specific categories")

                if hyponyms:

                    for item in hyponyms:
                        st.write("•", item)

                else:
                    st.warning("No hyponyms found.")


            # MEANINGS
            with word_tabs[7]:

                st.subheader("🧠 Different Meanings")

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

                            st.write("**Examples:**")

                            for example in meaning["examples"]:
                                st.write("•", example)


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

    if st.button("Tokenize Sentence"):

        if sentence.strip():

            tokens = nltk.word_tokenize(sentence)

            st.subheader("Tokens")

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
# TAB 3 - PARTS OF SPEECH
# =========================================================
with main_tabs[2]:

    st.header("🏷️ Parts of Speech Analysis")

    pos_sentence = st.text_area(
        "Enter a sentence for POS tagging:",
        placeholder="Example: Ali is reading a beautiful book."
    )

    if st.button("Analyze Parts of Speech"):

        if pos_sentence.strip():

            tokens = nltk.word_tokenize(
                pos_sentence
            )

            tags = nltk.pos_tag(tokens)

            st.subheader("POS Analysis")

            for word_item, tag in tags:

                meaning = pos_meanings.get(
                    tag,
                    "Punctuation or special symbol"
                )

                with st.container(border=True):

                    col1, col2, col3 = st.columns(
                        [2, 1, 4]
                    )

                    with col1:
                        st.write(
                            "**Word:**",
                            word_item
                        )

                    with col2:
                        st.write(
                            "**Tag:**",
                            tag
                        )

                    with col3:
                        st.write(
                            "**Meaning:**",
                            meaning
                        )

        else:

            st.warning(
                "Please enter a sentence."
            )


# =========================================================
# TAB 4 - SIMILARITY COMPARISON
# =========================================================
with main_tabs[3]:

    st.header("⚖️ Word Similarity Comparison")

    st.write(
        "Compare the semantic similarity of two words using WordNet."
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

    if st.button("Compare Similarity"):

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

                percentage = similarity * 100

                st.metric(
                    "Similarity Score",
                    f"{percentage:.2f}%"
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
                        "The words have low similarity."
                    )

        else:

            st.warning(
                "Please enter both words."
            )


# -----------------------------
# FOOTER
# -----------------------------
st.divider()

st.caption(
    "LexiScope | NLP Explorer | Streamlit + NLTK + WordNet"
)
