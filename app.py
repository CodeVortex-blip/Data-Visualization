import streamlit as st
import pdfplumber
import docx
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# --- Text Extraction ---
def extract_text(file):
    if file.name.endswith(".pdf"):
        with pdfplumber.open(file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text
    elif file.name.endswith(".docx"):
        doc = docx.Document(file)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        return ""

# --- Word Frequency ---
def get_word_freq(text, top_n=20):
    words = [word.lower() for word in text.split() if word.isalpha()]
    return Counter(words).most_common(top_n)

# --- WordCloud Plot ---
def plot_wordcloud(text):
    wc = WordCloud(width=800, height=400, background_color='white').generate(text)
    fig, ax = plt.subplots()
    ax.imshow(wc, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)

# --- Bar Chart ---
def plot_bar_chart(freq_data):
    words, counts = zip(*freq_data)
    fig, ax = plt.subplots()
    sns.barplot(x=list(counts), y=list(words), ax=ax)
    ax.set_title("Top Words - Bar Chart")
    st.pyplot(fig)

# --- Pie Chart ---
def plot_pie_chart(freq_data):
    words, counts = zip(*freq_data)
    fig, ax = plt.subplots()
    ax.pie(counts, labels=words, autopct='%1.1f%%', startangle=140)
    ax.set_title("Top Words - Pie Chart")
    st.pyplot(fig)

# --- Streamlit UI ---
st.title("📄 Document Visualizer")
st.markdown("Upload a PDF or DOCX file to generate visualizations.")

uploaded_file = st.file_uploader("Upload File", type=["pdf", "docx"])

if uploaded_file:
    text = extract_text(uploaded_file)
    if text:
        st.subheader("📃 Extracted Text Preview")
        st.text(text[:500] + "..." if len(text) > 500 else text)

        freq_data = get_word_freq(text)

        st.subheader("☁ Word Cloud")
        plot_wordcloud(text)

        st.subheader("📊 Bar Chart")
        plot_bar_chart(freq_data)

        st.subheader("🥧 Pie Chart")
        plot_pie_chart(freq_data)
    else:
        st.error("Could not extract text from the uploaded file.")
