import streamlit as st
from pathlib import Path
from PIL import Image
import requests
from bs4 import BeautifulSoup
from datetime import date
from transformers import pipeline
import matplotlib.pyplot as plt
import numpy as np
import re

news_sources = {
    "India (The Hindu)": "https://www.thehindu.com/news/national/",
    "USA (White House)": "https://www.whitehouse.gov/briefing-room/",
    "Pakistan (Dawn)": "https://www.dawn.com/world",
    "Bangladesh (Daily Star)": "https://www.thedailystar.net/news",
}

def fetch_news(url):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        if "thehindu.com" in url:
            articles = soup.select("h3 a")  
        elif "whitehouse.gov" in url:
            articles = soup.select("h2 a")  
        elif "dawn.com" in url:
            articles = soup.select("article h2 a")  
        elif "thedailystar.net" in url:
            articles = soup.select("h3.title a")  
        else:
            articles = []

        today = date.today().strftime("%Y-%m-%d")
        news_data = []
        for article in articles[:10]:  
            title = article.text.strip()
            link = article.get("href")
            full_link = link if link.startswith("http") else url + link
            news_data.append({
                "title": title,
                "link": full_link,
                "timestamp": today
            })
        return news_data

    except Exception as e:
        st.error(f"Error fetching news from {url}: {e}")
        return []

def extract_content(url):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        content = " ".join([p.get_text() for p in paragraphs])
        return preprocess_text(content)
    except Exception as e:
        st.error(f"Error extracting content from {url}: {e}")
        return ""

def preprocess_text(text):
    text = re.sub(r"\s+", " ", text)  
    text = re.sub(r"[^a-zA-Z0-9,.!? ]", "", text)  
    return text.strip()

def create_heatmap(image_path):
    try:
        image = Image.open(image_path)
        image_array = np.array(image.convert("L"))  
        plt.figure(figsize=(8, 6))
        plt.imshow(image_array, cmap="hot", interpolation="nearest")
        plt.axis("off")
        return plt
    except Exception as e:
        st.error(f"Error creating heatmap: {e}")
        return None

page = st.sidebar.selectbox("Navigate", ["Fetch News", "Heatmap Visualization"])

if page == "Fetch News":
    st.title("News Summarization")
    st.header("Today's News Summaries")

    if st.button("Fetch and Summarize News"):
        all_news = []
        for source, url in news_sources.items():
            news = fetch_news(url)
            if news:
                all_news.extend(news)
                st.success(f"Fetched {len(news)} articles from {source}")

        if all_news:
            summarizer = pipeline("summarization", model="t5-small", tokenizer="t5-small")
            st.subheader("Top News Summaries")

            for i, news in enumerate(all_news[:5]):
                content = extract_content(news["link"])
                if content:
                    summary = summarizer(content, max_length=80, min_length=20, do_sample=False)[0]["summary_text"]
                    st.write(f"{i+1}. {news['title']}")
                    st.write(f"[Read Full Article]({news['link']})")
                    st.write(f"Summary: {summary}")
                    st.write("---")

elif page == "Heatmap Visualization":
    st.title("Heatmap Visualization")
    st.header("Generated Heatmaps")

    image_paths = [
        "/Users/kdn_aikothalavanya/Downloads/WhatsApp Image 2025-03-07 at 15.25.22.jpeg",
        "/Users/kdn_aikothalavanya/Downloads/WhatsApp Image 2025-03-07 at 15.31.02.jpeg",
    ]

    for i, image_path in enumerate(image_paths, start=1):
        st.subheader(f"Heatmap {i}")
        heatmap_plot = create_heatmap(image_path)
        if heatmap_plot:
            st.pyplot(heatmap_plot)
