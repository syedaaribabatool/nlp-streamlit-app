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
    page_title="WordNet Explorer",
    page_icon="📚",
    layout="centered"
)

# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown("""
<style>

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
}

.sub-title {
    text-align: center;
    color: gray;
    margin-bottom: 25px;
}

.result-box {
    padding: 15px;
    border-radius: 10px;
    background-color: #f5f5f5;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------
# TITLE
# -----------------------------
st.markdown(
    '<div class="main-title">📚 WordNet Explorer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Explore words using the NLTK WordNet lexical database</div>',
    unsafe_allow_html=True
)


# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:

    st.header("About App")

    st.write(
        """
        This application uses WordNet to explore
        semantic relationships between English words.
        """
    )

    st.markdown("### Features")

    st.write("📘 Definitions")
    st.write("💬 Examples")
    st.write("🔄 Synonyms")
    st.write("↔️ Antonyms")
    st.write("⬆️ Hypernyms")
    st.write("⬇️ Hyponyms")
    st.write("🧠 Different Meanings")


# -----------------------------
# WORD INPUT
# -----------------------------
word = st.text_input(
    "🔍 Enter an English word",
    placeholder="Example: car, happy, bank"
)

word = word.strip().lower()


# -----------------------------
# FUNCTIONS
# -----------------------------

def get_definitions(word):

    definitions = []

    for synset in wordnet.synsets(word):
        definitions.append(synset.definition())

    return list(dict.fromkeys(definitions))


def get_examples(word):

    examples = []

    for synset in wordnet.synsets(word):
        for example in synset.examples():
            examples.append(example)

    return list(dict.fromkeys(examples))


def get_synonyms(word):

    synonyms = set()

    for synset in wordnet.synsets(word):

        for lemma in synset.lemmas():

            synonym = lemma.name().replace("_", " ")

            synonyms.add(synonym)

    return sorted(synonyms)


def get_antonyms(word):

    antonyms = set()

    for synset in wordnet.synsets(word):

        for lemma in synset.lemmas():

            for antonym in lemma.antonyms():

                antonyms.add(
                    antonym.name().replace("_", " ")
                )

    return sorted(antonyms)


def get_hypernyms(word):

    hypernyms = set()

    for synset in wordnet.synsets(word):

        for hypernym in synset.hypernyms():

            for lemma in hypernym.lemmas():

                hypernyms.add(
                    lemma.name().replace("_", " ")
                )

    return sorted(hypernyms)


def get_hyponyms(word):

    hyponyms = set()

    for synset in wordnet.synsets(word):

        for hyponym in synset.hyponyms():

            for lemma in hyponym.lemmas():

                hyponyms.add(
                    lemma.name().replace("_", " ")
                )

    return sorted(hyponyms)


def get_meanings(word):

    meanings = []

    for synset in wordnet.synsets(word):

        meanings.append({
            "name": synset.name(),
            "part_of_speech": synset.pos(),
            "definition": synset.definition()
        })

    return meanings


# -----------------------------
# BUTTONS
# -----------------------------
st.markdown("### Choose an option")

col1, col2, col3 = st.columns(3)

with col1:
    definition_button = st.button(
        "📘 Definition",
        use_container_width=True
    )

with col2:
    example_button = st.button(
        "💬 Examples",
        use_container_width=True
    )

with col3:
    synonym_button = st.button(
        "🔄 Synonyms",
        use_container_width=True
    )


col4, col5, col6 = st.columns(3)

with col4:
    antonym_button = st.button(
        "↔️ Antonyms",
        use_container_width=True
    )

with col5:
    hypernym_button = st.button(
        "⬆️ Hypernyms",
        use_container_width=True
    )

with col6:
    hyponym_button = st.button(
        "⬇️ Hyponyms",
        use_container_width=True
    )


meaning_button = st.button(
    "🧠 Different Meanings",
    use_container_width=True
)


# -----------------------------
# RESULTS
# -----------------------------
if word:

    synsets = wordnet.synsets(word)

    if not synsets:

        st.error(
            f'No WordNet information found for "{word}".'
        )

    else:

        st.success(
            f'Word found: "{word}"'
        )

        # Definitions
        if definition_button:

            st.markdown("## 📘 Definitions")

            definitions = get_definitions(word)

            for i, definition in enumerate(
                definitions, start=1
            ):

                st.info(
                    f"{i}. {definition}"
                )


        # Examples
        if example_button:

            st.markdown("## 💬 Examples")

            examples = get_examples(word)

            if examples:

                for i, example in enumerate(
                    examples, start=1
                ):

                    st.success(
                        f'{i}. "{example}"'
                    )

            else:

                st.warning(
                    "No example sentences are available."
                )


        # Synonyms
        if synonym_button:

            st.markdown("## 🔄 Synonyms")

            synonyms = get_synonyms(word)

            if synonyms:

                st.write(
                    ", ".join(synonyms)
                )

                st.caption(
                    f"Total synonyms found: {len(synonyms)}"
                )

            else:

                st.warning(
                    "No synonyms found."
                )


        # Antonyms
        if antonym_button:

            st.markdown("## ↔️ Antonyms")

            antonyms = get_antonyms(word)

            if antonyms:

                st.write(
                    ", ".join(antonyms)
                )

                st.caption(
                    f"Total antonyms found: {len(antonyms)}"
                )

            else:

                st.warning(
                    "No antonyms found."
                )


        # Hypernyms
        if hypernym_button:

            st.markdown("## ⬆️ Hypernyms")

            st.caption(
                "Hypernyms are broader categories."
            )

            hypernyms = get_hypernyms(word)

            if hypernyms:

                st.write(
                    ", ".join(hypernyms)
                )

            else:

                st.warning(
                    "No hypernyms found."
                )


        # Hyponyms
        if hyponym_button:

            st.markdown("## ⬇️ Hyponyms")

            st.caption(
                "Hyponyms are more specific words."
            )

            hyponyms = get_hyponyms(word)

            if hyponyms:

                st.write(
                    ", ".join(hyponyms)
                )

            else:

                st.warning(
                    "No hyponyms found."
                )


        # Different meanings
        if meaning_button:

            st.markdown(
                "## 🧠 Different Meanings"
            )

            meanings = get_meanings(word)

            for i, meaning in enumerate(
                meanings, start=1
            ):

                with st.expander(
                    f"Meaning {i} — {meaning['name']}"
                ):

                    st.write(
                        "**Part of Speech:**",
                        meaning["part_of_speech"]
                    )

                    st.write(
                        "**Definition:**",
                        meaning["definition"]
                    )


else:

    st.info(
        "Enter a word above and click any button."
    )


# -----------------------------
# FOOTER
# -----------------------------
st.divider()

st.caption(
    "WordNet Explorer | Built with Streamlit + NLTK"
)
