import requests
from bs4 import BeautifulSoup
from datetime import datetime, date
from transformers import pipeline
import smtplib
from email.message import EmailMessage
import json
import re


news_sources = {
    "India (The Hindu)": "https://www.thehindu.com/news/national/",
    "USA (White House)": "https://www.whitehouse.gov/briefing-room/",
    "UK (BBC Politics)": "https://www.bbc.com/news/politics",
    "Pakistan (Dawn)": "https://www.dawn.com/world",
    "Bangladesh (Daily Star)": "https://www.thedailystar.net/news",
}


es_url = "http://localhost:9200/news_data/_doc"


def fetch_news(url):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        if "thehindu.com" in url:
            articles = soup.select("h3 a")
        elif "whitehouse.gov" in url:
            articles = soup.select("h2 a")
        elif "bbc.com" in url:
            articles = soup.select("h3 a")
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
        print(f"Error fetching news from {url}: {e}")
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
        print(f"Error extracting content from {url}: {e}")
        return ""


def preprocess_text(text):
    text = re.sub(r"\s+", " ", text)  
    text = re.sub(r"[^a-zA-Z0-9,.!? ]", "", text)  
    return text.strip()


def store_in_elasticsearch(data):
    for record in data:
        response = requests.post(es_url, json=record, headers={"Content-Type": "application/json"})
        if response.status_code == 201:
            print(f"Stored record: {record['title']}")
        else:
            print(f"Failed to store record: {response.text}")


def fetch_and_store_news():
    all_news = []
    for source, url in news_sources.items():
        news = fetch_news(url)
        for article in news:
            article["content"] = extract_content(article["link"])
        all_news.extend(news)
    store_in_elasticsearch(all_news)


def fetch_preprocessed_data():
    headers = {"Content-Type": "application/json"}
    today = date.today().strftime("%Y-%m-%d")
    query = {
        "query": {"match": {"timestamp": today}},
        "size": 10
    }
    response = requests.post(f"{es_url}/_search", headers=headers, json=query)
    if response.status_code == 200:
        data = response.json()
        return [(hit["_source"]["title"], hit["_source"].get("content", "")) for hit in data["hits"]["hits"]]
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return []


def summarize_data(preprocessed_articles):
    summarizer = pipeline("summarization", model="t5-small", tokenizer="t5-small")
    summaries = []
    for title, content in preprocessed_articles:
        summary = summarizer(content, max_length=50, min_length=10, do_sample=False)
        summaries.append(f"{title}: {summary[0]['summary_text']}")
    return summaries


def send_email_alerts(subject, summaries, to):
    numbered_summaries = "\n".join([f"{i + 1}. {summary}" for i, summary in enumerate(summaries)])
    msg = EmailMessage()
    msg.set_content(numbered_summaries)
    msg["subject"] = subject
    msg["to"] = to
    msg["from"] = "kothalavanya99@gmail.com"
    password = "xjrkqxvcntwkgntm"
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(msg["from"], password)
        server.send_message(msg)
        server.quit()
        print(f"Email sent to {to}")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    print("Fetching and storing news...")
    fetch_and_store_news()
    
    print("Fetching preprocessed data...")
    preprocessed_articles = fetch_preprocessed_data()
    if not preprocessed_articles:
        print("No data found.")
        exit()
    
    print("Summarizing content...")
    summaries = summarize_data(preprocessed_articles)
    
    print("Sending email...")
    send_email_alerts("Today's News Summaries", summaries, "lavanya.21bce9452@vitapstudent.ac.in")
