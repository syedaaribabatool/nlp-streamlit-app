import streamlit as st
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet

nltk.download("punkt")
nltk.download("punkt_tab")
nltk.download("wordnet")

st.title("NLP Web Application")

sentence = st.text_input("Enter desired sentence:")

operation = st.selectbox(
    "Select NLP Operation",
    ["Tokenization", "Synonym", "Antonym"]
)

if st.button("Process"):

    if sentence == "":
        st.warning("Please enter a sentence.")

    elif operation == "Tokenization":
        tokens = word_tokenize(sentence)
        st.subheader("Tokens")
        st.write(tokens)

    elif operation == "Synonym":
        words = word_tokenize(sentence)

        st.subheader("Synonyms")

        for word in words:
            synonyms = set()

            for syn in wordnet.synsets(word):
                for lemma in syn.lemmas():
                    synonyms.add(lemma.name())

            if synonyms:
                st.write(f"{word}: {list(synonyms)[:5]}")
            else:
                st.write(f"{word}: No synonym found")

    elif operation == "Antonym":
        words = word_tokenize(sentence)

        st.subheader("Antonyms")

        for word in words:
            antonyms = set()

            for syn in wordnet.synsets(word):
                for lemma in syn.lemmas():
                    for antonym in lemma.antonyms():
                        antonyms.add(antonym.name())

            if antonyms:
                st.write(f"{word}: {list(antonyms)}")
            else:
                st.write(f"{word}: No antonym found")
