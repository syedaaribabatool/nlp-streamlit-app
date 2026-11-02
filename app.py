import streamlit as st
import nltk
from nltk.corpus import wordnet

# -----------------------------
# DOWNLOAD WORDNET
# -----------------------------
nltk.download("wordnet", quiet=True)

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="LexiScope - WordNet Explorer",
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

div.stButton > button {
    border-radius: 8px;
    height: 42px;
    font-weight: 600;
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
        definition = syn.definition()

        if definition:
            definitions.append(definition)

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

            synonym = lemma.name().replace("_", " ")
            synonyms.add(synonym)

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


# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:

    st.title("📘 LexiScope")

    st.caption(
        "A WordNet-based lexical and semantic exploration tool."
    )

    st.divider()

    st.subheader("Features")

    st.write("📘 Definitions")
    st.write("💬 Example Sentences")
    st.write("🔄 Synonyms")
    st.write("↔️ Antonyms")
    st.write("⬆️ Hypernyms")
    st.write("⬇️ Hyponyms")
    st.write("🧠 Different Meanings")

    st.divider()

    st.info(
        "Try words such as: "
        "`bank`, `car`, `run`, `good`, `light`."
    )


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
    Explore the meaning and semantic relationships of English words using WordNet
    </div>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# SEARCH AREA
# -----------------------------
search_col1, search_col2 = st.columns([5, 1])

with search_col1:

    word = st.text_input(
        "Enter a word",
        placeholder="Enter an English word...",
        label_visibility="collapsed"
    )

with search_col2:

    search_button = st.button(
        "🔍 Search",
        use_container_width=True,
        type="primary"
    )

word = word.strip().lower()


# -----------------------------
# MAIN APPLICATION
# -----------------------------
if word:

    synsets = get_synsets(word)

    if not synsets:

        st.error(
            f'No WordNet information was found for "{word}".'
        )

    else:

        definitions = get_definitions(word)
        examples = get_examples(word)
        synonyms = get_synonyms(word)
        antonyms = get_antonyms(word)
        hypernyms = get_hypernyms(word)
        hyponyms = get_hyponyms(word)
        meanings = get_meanings(word)

        # -----------------------------
        # WORD SUMMARY
        # -----------------------------
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
                    {len(meanings)} WordNet meaning(s) found
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        # -----------------------------
        # METRIC CARDS
        # -----------------------------
        m1, m2, m3, m4 = st.columns(4)

        with m1:
            st.metric(
                "Meanings",
                len(meanings)
            )

        with m2:
            st.metric(
                "Synonyms",
                len(synonyms)
            )

        with m3:
            st.metric(
                "Antonyms",
                len(antonyms)
            )

        with m4:
            st.metric(
                "Examples",
                len(examples)
            )

        st.write("")

        # -----------------------------
        # TABS
        # -----------------------------
        tabs = st.tabs([
            "🏠 Overview",
            "📘 Definitions",
            "💬 Examples",
            "🔄 Synonyms",
            "↔️ Antonyms",
            "⬆️ Hypernyms",
            "⬇️ Hyponyms",
            "🧠 Meanings"
        ])


        # -----------------------------
        # OVERVIEW
        # -----------------------------
        with tabs[0]:

            st.subheader("Word Overview")

            if definitions:

                st.markdown("#### Primary Definition")
                st.info(definitions[0])

            col1, col2 = st.columns(2)

            with col1:

                st.markdown("#### Synonyms")

                if synonyms:

                    st.write(
                        ", ".join(synonyms[:10])
                    )

                else:

                    st.caption(
                        "No synonyms available."
                    )

            with col2:

                st.markdown("#### Antonyms")

                if antonyms:

                    st.write(
                        ", ".join(antonyms[:10])
                    )

                else:

                    st.caption(
                        "No antonyms available."
                    )


        # -----------------------------
        # DEFINITIONS - FIXED
        # -----------------------------
        with tabs[1]:

            st.subheader("📘 Definitions")

            st.caption(
                f"Definitions available for '{word}'"
            )

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
                    "No definitions were found."
                )


        # -----------------------------
        # EXAMPLES - FIXED
        # -----------------------------
        with tabs[2]:

            st.subheader("💬 Example Sentences")

            st.caption(
                f"Examples available for '{word}'"
            )

            if examples:

                for i, example in enumerate(
                    examples,
                    start=1
                ):

                    with st.container(border=True):

                        st.markdown(
                            f"**Example {i}**"
                        )

                        st.write(
                            f'"{example}"'
                        )

            else:

                st.warning(
                    "WordNet does not provide example sentences for this word."
                )


        # -----------------------------
        # SYNONYMS
        # -----------------------------
        with tabs[3]:

            st.subheader("🔄 Synonyms")

            st.caption(
                "Words with similar meanings."
            )

            if synonyms:

                for synonym in synonyms:

                    st.write(
                        "•", synonym
                    )

                st.success(
                    f"{len(synonyms)} synonym(s) found."
                )

            else:

                st.warning(
                    "No synonyms found."
                )


        # -----------------------------
        # ANTONYMS
        # -----------------------------
        with tabs[4]:

            st.subheader("↔️ Antonyms")

            st.caption(
                "Words with opposite meanings."
            )

            if antonyms:

                for antonym in antonyms:

                    st.write(
                        "•", antonym
                    )

                st.success(
                    f"{len(antonyms)} antonym(s) found."
                )

            else:

                st.warning(
                    "No antonyms are available for this word."
                )


        # -----------------------------
        # HYPERNYMS
        # -----------------------------
        with tabs[5]:

            st.subheader("⬆️ Hypernyms")

            st.caption(
                "Hypernyms are broader or more general categories."
            )

            if hypernyms:

                for item in hypernyms:

                    st.write(
                        "•", item
                    )

            else:

                st.warning(
                    "No hypernyms found."
                )


        # -----------------------------
        # HYPONYMS
        # -----------------------------
        with tabs[6]:

            st.subheader("⬇️ Hyponyms")

            st.caption(
                "Hyponyms are more specific words or subcategories."
            )

            if hyponyms:

                for item in hyponyms:

                    st.write(
                        "•", item
                    )

            else:

                st.warning(
                    "No hyponyms found."
                )


        # -----------------------------
        # DIFFERENT MEANINGS
        # -----------------------------
        with tabs[7]:

            st.subheader(
                "🧠 Different Meanings"
            )

            st.caption(
                "A word can have multiple meanings depending on context."
            )

            for i, meaning in enumerate(
                meanings,
                start=1
            ):

                with st.expander(
                    f"Meaning {i} — "
                    f"{meaning['part_of_speech']} "
                    f"({meaning['synset']})"
                ):

                    st.markdown(
                        "**Definition**"
                    )

                    st.write(
                        meaning["definition"]
                    )

                    if meaning["examples"]:

                        st.markdown(
                            "**Examples**"
                        )

                        for example in meaning["examples"]:

                            st.write(
                                "•", example
                            )

                    else:

                        st.caption(
                            "No example available for this meaning."
                        )


else:

    st.info(
        "👆 Enter an English word above to start exploring."
    )


# -----------------------------
# FOOTER
# -----------------------------
st.divider()

st.caption(
    "LexiScope | WordNet Explorer | Built with Streamlit + NLTK"
)
