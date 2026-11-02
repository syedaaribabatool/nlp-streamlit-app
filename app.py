import streamlit as st
import nltk
from nltk.corpus import wordnet

# Download WordNet
nltk.download("wordnet")

# Page settings
st.set_page_config(
    page_title="WordNet Explorer",
    page_icon="📖",
    layout="centered"
)

# Title
st.title("📖 WordNet Explorer")
st.write("Enter an English word and select what you want to explore.")

# Input word
word = st.text_input("Enter a word:", placeholder="e.g. car, happy, bank")

# -----------------------------
# FUNCTIONS
# -----------------------------

def get_definitions(word):
    definitions = []

    for syn in wordnet.synsets(word):
        definitions.append(syn.definition())

    return definitions


def get_examples(word):
    examples = set()

    for syn in wordnet.synsets(word):
        for example in syn.examples():
            examples.add(example)

    return sorted(examples)


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

    for syn in wordnet.synsets(word):
        meanings.append(
            f"{syn.name()} → {syn.definition()}"
        )

    return meanings


# -----------------------------
# BUTTONS
# -----------------------------

col1, col2 = st.columns(2)

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


col3, col4 = st.columns(2)

with col3:
    synonym_button = st.button(
        "🔄 Synonyms",
        use_container_width=True
    )

with col4:
    antonym_button = st.button(
        "↔️ Antonyms",
        use_container_width=True
    )


col5, col6 = st.columns(2)

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
# CHECK WORD
# -----------------------------

if word:

    synsets = wordnet.synsets(word)

    if not synsets:

        st.error("Word not found in WordNet.")

    else:

        # Definition
        if definition_button:

            st.subheader("📘 Definitions")

            definitions = get_definitions(word)

            for i, definition in enumerate(
                definitions, 1
            ):
                st.write(
                    f"{i}. {definition}"
                )


        # Examples
        if example_button:

            st.subheader("💬 Examples")

            examples = get_examples(word)

            if examples:

                for example in examples:
                    st.write("•", example)

            else:
                st.info(
                    "No examples available."
                )


        # Synonyms
        if synonym_button:

            st.subheader("🔄 Synonyms")

            synonyms = get_synonyms(word)

            if synonyms:

                for synonym in synonyms:
                    st.write("•", synonym)

            else:
                st.info(
                    "No synonyms found."
                )


        # Antonyms
        if antonym_button:

            st.subheader("↔️ Antonyms")

            antonyms = get_antonyms(word)

            if antonyms:

                for antonym in antonyms:
                    st.write("•", antonym)

            else:
                st.info(
                    "No antonyms found."
                )


        # Hypernyms
        if hypernym_button:

            st.subheader("⬆️ Hypernyms")

            st.write(
                "Broader categories:"
            )

            hypernyms = get_hypernyms(word)

            if hypernyms:

                for hypernym in hypernyms:
                    st.write(
                        "•", hypernym
                    )

            else:
                st.info(
                    "No hypernyms found."
                )


        # Hyponyms
        if hyponym_button:

            st.subheader("⬇️ Hyponyms")

            st.write(
                "More specific words:"
            )

            hyponyms = get_hyponyms(word)

            if hyponyms:

                for hyponym in hyponyms:
                    st.write(
                        "•", hyponym
                    )

            else:
                st.info(
                    "No hyponyms found."
                )


        # Different Meanings
        if meaning_button:

            st.subheader(
                "🧠 Different Meanings"
            )

            meanings = get_meanings(word)

            for i, meaning in enumerate(
                meanings, 1
            ):
                st.write(
                    f"{i}. {meaning}"
                )

else:

    st.info(
        "Enter a word first, then click any button."
    )
