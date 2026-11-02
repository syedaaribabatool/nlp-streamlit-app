import streamlit as st
import nltk
from nltk.corpus import wordnet

# -----------------------------
# SETUP
# -----------------------------
nltk.download("wordnet", quiet=True)

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
    font-size: 45px;
    font-weight: 700;
    margin-bottom: 0px;
}

.subtitle {
    font-size: 17px;
    color: #6c757d;
    margin-top: 5px;
    margin-bottom: 30px;
}

.section-title {
    font-size: 24px;
    font-weight: 600;
    margin-top: 20px;
}

.info-card {
    padding: 18px;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    background-color: #fafafa;
    margin-bottom: 12px;
}

.word-box {
    padding: 18px;
    border-radius: 12px;
    background-color: #f4f6f8;
    border-left: 5px solid #4b5563;
    margin-top: 15px;
}

.small-text {
    font-size: 14px;
    color: #6c757d;
}

div.stButton > button {
    border-radius: 8px;
    height: 42px;
    font-weight: 500;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------
# FUNCTIONS
# -----------------------------
def get_synsets(word):
    return wordnet.synsets(word)


def get_definitions(word):
    return list(dict.fromkeys(
        syn.definition()
        for syn in wordnet.synsets(word)
    ))


def get_examples(word):
    examples = []

    for syn in wordnet.synsets(word):
        examples.extend(syn.examples())

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
    data = []

    pos_names = {
        "n": "Noun",
        "v": "Verb",
        "a": "Adjective",
        "s": "Adjective",
        "r": "Adverb"
    }

    for syn in wordnet.synsets(word):

        data.append({
            "synset": syn.name(),
            "part_of_speech": pos_names.get(
                syn.pos(), syn.pos()
            ),
            "definition": syn.definition(),
            "examples": syn.examples()
        })

    return data


# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:

    st.title("LexiScope")

    st.caption(
        "A semantic word exploration tool powered by NLTK WordNet."
    )

    st.divider()

    st.subheader("What can you explore?")

    st.write("• Definitions")
    st.write("• Example sentences")
    st.write("• Synonyms")
    st.write("• Antonyms")
    st.write("• Hypernyms")
    st.write("• Hyponyms")
    st.write("• Multiple word meanings")

    st.divider()

    st.info(
        "Tip: Try words such as "
        "`bank`, `car`, `light`, `good`, or `run`."
    )


# -----------------------------
# HEADER
# -----------------------------
st.markdown(
    '<div class="main-title">LexiScope</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
    Professional WordNet Explorer for semantic and lexical analysis
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
        "Search a word",
        placeholder="Enter an English word...",
        label_visibility="collapsed"
    )

with search_col2:
    search_button = st.button(
        "Search",
        use_container_width=True,
        type="primary"
    )

word = word.strip().lower()


# -----------------------------
# PROCESS
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

        # -------------------------
        # WORD SUMMARY
        # -------------------------
        st.markdown(
            f"""
            <div class="word-box">
                <div style="font-size:14px;color:#6c757d;">
                    Search Result
                </div>
                <div style="font-size:30px;font-weight:700;">
                    {word.title()}
                </div>
                <div class="small-text">
                    Found {len(synsets)} WordNet meaning(s)
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        # -------------------------
        # METRICS
        # -------------------------
        m1, m2, m3, m4 = st.columns(4)

        m1.metric(
            "Meanings",
            len(meanings)
        )

        m2.metric(
            "Synonyms",
            len(synonyms)
        )

        m3.metric(
            "Antonyms",
            len(antonyms)
        )

        m4.metric(
            "Examples",
            len(examples)
        )

        st.write("")

        # -------------------------
        # TABS
        # -------------------------
        tabs = st.tabs([
            "Overview",
            "Definitions",
            "Examples",
            "Synonyms",
            "Antonyms",
            "Hypernyms",
            "Hyponyms",
            "Meanings"
        ])

        # -------------------------
        # OVERVIEW
        # -------------------------
        with tabs[0]:

            st.subheader("Word Overview")

            if definitions:
                st.write("**Primary Definition**")
                st.info(definitions[0])

            col1, col2 = st.columns(2)

            with col1:

                st.write("**Synonyms**")

                if synonyms:
                    st.write(", ".join(synonyms[:10]))

                else:
                    st.caption("No synonyms found.")

            with col2:

                st.write("**Antonyms**")

                if antonyms:
                    st.write(", ".join(antonyms[:10]))

                else:
                    st.caption("No antonyms found.")

        # -------------------------
        # DEFINITIONS
        # -------------------------
        with tabs[1]:

            st.subheader("Definitions")

            for i, definition in enumerate(
                definitions, start=1
            ):

                st.markdown(
                    f"""
                    <div class="info-card">
                    <b>Definition {i}</b><br><br>
                    {definition}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # -------------------------
        # EXAMPLES
        # -------------------------
        with tabs[2]:

            st.subheader("Example Sentences")

            if examples:

                for i, example in enumerate(
                    examples, start=1
                ):
                    st.markdown(
                        f"""
                        <div class="info-card">
                        <b>Example {i}</b><br>
                        "{example}"
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            else:

                st.info(
                    "No example sentences are available."
                )

        # -------------------------
        # SYNONYMS
        # -------------------------
        with tabs[3]:

            st.subheader("Synonyms")

            st.caption(
                "Words with similar meanings."
            )

            if synonyms:

                for synonym in synonyms:
                    st.write("•", synonym)

            else:
                st.info("No synonyms found.")

        # -------------------------
        # ANTONYMS
        # -------------------------
        with tabs[4]:

            st.subheader("Antonyms")

            st.caption(
                "Words with opposite meanings."
            )

            if antonyms:

                for antonym in antonyms:
                    st.write("•", antonym)

            else:
                st.info("No antonyms found.")

        # -------------------------
        # HYPERNYMS
        # -------------------------
        with tabs[5]:

            st.subheader("Hypernyms")

            st.caption(
                "Broader or more general categories."
            )

            if hypernyms:

                for item in hypernyms:
                    st.write("•", item)

            else:
                st.info("No hypernyms found.")

        # -------------------------
        # HYPONYMS
        # -------------------------
        with tabs[6]:

            st.subheader("Hyponyms")

            st.caption(
                "More specific words or subcategories."
            )

            if hyponyms:

                for item in hyponyms:
                    st.write("•", item)

            else:
                st.info("No hyponyms found.")

        # -------------------------
        # DIFFERENT MEANINGS
        # -------------------------
        with tabs[7]:

            st.subheader("Different Meanings")

            for i, meaning in enumerate(
                meanings, start=1
            ):

                with st.expander(
                    f"{i}. {meaning['part_of_speech']} — "
                    f"{meaning['synset']}"
                ):

                    st.write(
                        "**Definition:**",
                        meaning["definition"]
                    )

                    if meaning["examples"]:

                        st.write("**Examples:**")

                        for example in meaning["examples"]:
                            st.write("•", example)

else:

    st.info(
        "Enter an English word above to begin exploring WordNet."
    )

# -----------------------------
# FOOTER
# -----------------------------
st.divider()

st.caption(
    "LexiScope • WordNet Explorer • Built using Streamlit and NLTK"
)
