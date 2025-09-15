import streamlit as st
import docx2txt
import pdfplumber
import matplotlib.pyplot as plt
from collections import Counter
import re

# Function to extract text from PDF using pdfplumber
def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

# Function to extract text from DOCX
def extract_text_from_docx(file):
    return docx2txt.process(file)

# Function to clean and tokenize text
def tokenize(text):
    text = re.sub(r'[^A-Za-z\s]', '', text)
    words = text.lower().split()
    return words

# Function to plot word frequency
def plot_word_freq(words, top_n=20):
    freq = Counter(words)
    common = freq.most_common(top_n)
    labels, counts = zip(*common)
    fig, ax = plt.subplots()
    ax.barh(labels[::-1], counts[::-1])
    ax.set_title(f"Top {top_n} Words")
    st.pyplot(fig)

# Streamlit UI
st.title("📄 Text Visualization from PDF/DOCX")
uploaded_file = st.file_uploader("Upload a PDF or DOCX file", type=["pdf", "docx"])

if uploaded_file:
    if uploaded_file.name.endswith(".pdf"):
        text = extract_text_from_pdf(uploaded_file)
    else:
        text = extract_text_from_docx(uploaded_file)

    st.subheader("Extracted Text (Preview)")
    st.write(text[:1000] + "...")  # Show first 1000 characters

    words = tokenize(text)
    st.subheader("Word Frequency Visualization")
    plot_word_freq(words)
